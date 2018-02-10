import json
import time
import os
import uuid
import io

from .aws import (
        delete_s3_object,
        download_from_s3,
        list_s3_bucket,
        invoke_lambda,
        read_from_s3,
        read_body_from_s3,
        s3_file_exists,
        write_to_s3,
        write_csv_to_s3,
)


def _get_final_results_key(run_id):
    return 'run-%s/FinalResults.json' % (run_id, )


def _get_batch_job_prefix(run_id):
    return 'run-%s/mapper-' % (run_id, )


def _get_job_metadata(event):
    s3_record = event['Records'][0]['s3']
    bucket = s3_record['bucket']['name']
    key = s3_record['object']['key']

    s3_obj = read_from_s3(bucket, key)
    job_metadata = s3_obj['Metadata']

    run_id = job_metadata['run_id']
    total_jobs = int(job_metadata['total_jobs'])
    return (bucket, run_id, total_jobs)


def reduce(event):
    bucket, run_id, total_jobs = _get_job_metadata(event)

    # count up all of the final done files and make sure they equal the total number of mapper jobs
    prefix = _get_batch_job_prefix(run_id)
    final_files = [
            (bucket, key) for (_, key) in \
            list_s3_bucket(bucket, prefix) \
            if key.endswith('-final-done.csv')
    ]
    if len(final_files) != total_jobs:
        print(
            'Reducers are still running...skipping. Expected %d done files but found %s' % (
                total_jobs, len(final_files),
            )
        )
        return

    # Let's put a lock file here so we can claim that we're finishing up the final reduce step
    final_results_key = _get_final_results_key(run_id)
    if s3_file_exists(bucket, final_results_key):
        print('Skipping final reduce step')
        return

    print('Starting final reduce phase')

    chunk_size = 10
    s3_mapper_files = list_s3_bucket(bucket, prefix)

    chunks = [s3_mapper_files[i: i+chunk_size] for i in range(0, len(s3_mapper_files), chunk_size)]
    total_chunks = len(chunks)

    for i, chunk in enumerate(chunks):
        payload = {
                's3_files': chunk,
                'total_chunks': total_chunks,
                'chunk_number': i + 1,
                'bucket': bucket,
                'run_id': run_id,
        }
        print('Invoke final reducer', payload)
        invoke_lambda('map-reduce-dev-FinalReducer', payload)


def final_reducer(event):
    print('Received event')
    print(event)

    s3_files = event['s3_files']
    total_chunks = event['total_chunks']
    chunk_number = event['chunk_number']
    bucket = event['bucket']
    run_id = event['run_id']
    level = int(event.get('level', 1))

    prefix = 'run-%s' % (run_id, )

    print('Chunk %s of %s' % (chunk_number, total_chunks))

    results = {}

    for (bucket, key) in s3_files:
        print('reading', key)

        #data = json.loads(read_body_from_s3(bucket, key))
        fn = download_from_s3(bucket, key)

        print('Deleting %s' % (key, ))
        delete_s3_object(bucket, key)

        with open(fn, 'r') as fh:
            for line in fh:
                ip, score = line.split(',')
                ip = int(ip)
                score = float(score)

                if ip in results:
                    results[ip] += score
                else:
                    results[ip] = score

        os.remove(fn)

        # if not results:
        #     results = data
        #     continue

        # for ip, score in data.items():
        #     try:
        #         results[ip] += float(score)
        #     except KeyError:
        #         results[ip] = float(score)

    print('Final results:', len(results))
    print('Writing fiinal output data')
    #results_key = '%s/reducer-l%s-%s.json' % (prefix, level, chunk_number)
    results_key = '%s/reducer-l%s-%s.csv' % (prefix, level, chunk_number)
    metadata = {
            'total_chunks': str(total_chunks),
            'chunk_number': str(chunk_number),
    }
    write_csv_to_s3(bucket, results_key, results, Metadata=metadata)

    reducer_prefix = '%s/reducer-l%s' % (prefix, level)
    finished_reducers = list_s3_bucket(bucket, reducer_prefix)
    num_finished = len(finished_reducers)

    print('Total number of reduced files:', num_finished)
    print('All done?', num_finished == int(total_chunks))

    chunk_size = 2
    if num_finished == int(total_chunks):
        chunks = [finished_reducers[i: i+chunk_size] for i in range(0, num_finished, chunk_size)]
        total_chunks = len(chunks)
        if total_chunks == 1:
            print('Total chunks is one', total_chunks)
            return

        for i, chunk in enumerate(chunks):
            if len(chunk) == 1:
                print('Chunk of size 1')
                print(chunk)
                continue

            payload = {
                    's3_files': chunk,
                    'total_chunks': total_chunks,
                    'chunk_number': i + 1,
                    'bucket': bucket,
                    'run_id': run_id,
                    'level': level + 1,
            }
            print(payload)
            invoke_lambda('map-reduce-dev-FinalReducer', payload)
