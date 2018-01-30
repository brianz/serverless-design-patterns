import json
import time
import uuid

from .aws import (
        download_from_s3,
        list_s3_bucket,
        read_from_s3,
        s3_file_exists,
        write_to_s3,
)


# def reduce(event):
#     """First stage reducer.
#
#     This reducer will write it's results to the results bucket. There needs to be a final reduce
#     step which will only be called once all intermediate reducers have finished writing to S3. The
#     final reducer is responsible for checking whether all reducers are finished.
#
#     """
#     bucket = 'brianz-dev-mapreduce-results'
#
#     job_id = event['job_id']
#     run_id = event['run_id']
#     payload = event['payload']
#     batch = event['batch']
#
#     key = 'run-%s/job-%s-payload-%s.json' % (run_id, job_id, batch)
#     write_to_s3(bucket, key, payload)



def batch_reducer(job_metadata):
    # s3_record = event['Records'][0]['s3']
    # bucket = s3_record['bucket']['name']
    # key = s3_record['object']['key']

    # ensure we're only processing results once they are finished. This file is placed in S3 from
    # the mapper step and signifies that all of the mappers have completed their job, getting
    # through the entire list of batched maps
    # if not key.endswith('-batch-done.json'):
    #     return

    # print('Kicking off batch reducer for: %s %s' % (bucket, key, ))

    # job_metadata = json.loads(read_from_s3(bucket, key))

    expected_batches = int(job_metadata['batches'])
    job_id = job_metadata['job_id']
    run_id = job_metadata['run_id']
    total_jobs = job_metadata['total_jobs']
    bucket = job_metadata['bucket']

    prefix = 'run-%s/job-%s' % (run_id, job_id)

    final_data = {}
    runs = 0
    for _, key in list_s3_bucket(bucket, prefix):
        if key.endswith('-done.json'):
            continue

        payload = json.loads(read_from_s3(bucket, key))
        data = payload['data']
        runs += 1

        if not final_data:
            #print(bucket, key)
            final_data = data
            continue

        for ip, score in data.items():
            final_data.setdefault(ip, 0)
            final_data[ip] += float(score)

    print(expected_batches == runs, expected_batches, runs)

    key = 'run-%s/batch-job-%s-final-done.json' % (run_id, job_id)
    write_to_s3(bucket, key, {
        'data': final_data,
        'run_id': run_id,
        'total_jobs': total_jobs,

    })



def final_reducer(event):
    s3_record = event['Records'][0]['s3']
    bucket = s3_record['bucket']['name']
    key = s3_record['object']['key']

    job_metadata = json.loads(read_from_s3(bucket, key))

    run_id = job_metadata['run_id']
    total_jobs = int(job_metadata['total_jobs'])

    # count up all of the final done files and make sure they equal the total number of mapper jobs
    prefix = 'run-%s/batch-job-' % (run_id, )
    time.sleep(2)
    final_files = [
            (bucket, key) for (_, key) in \
            list_s3_bucket(bucket, prefix) \
            if key.endswith('-final-done.json')
    ]
    if len(final_files) != total_jobs:
        print(
            'Reducers are still running...skipping. Expected %d done files but found %s' % (
                total_jobs, len(final_files),
            )
        )
        return

    import gc
    job_metadata = {}
    gc.collect()

    # Let's put a lock file here so we can claim that we're finishing up the final reduce step
    final_results_key = 'run-%s/FinalResults.json' % (run_id, )
    if s3_file_exists(bucket, final_results_key):
        print('Skipping final reduce step')
        return

    write_to_s3(bucket, final_results_key, {'run_id': run_id})

    final_data = {}
    data = {}

    print('listing', bucket, prefix)

    temp_file_names = []

    for (bucket, key) in list_s3_bucket(bucket, prefix):
        print('reading', key)
        if not key.endswith('-final-done.json'):
            continue

        # it can take a while for the data to be read consistently from S3, so in the case that
        # there is no data wait a bit.
        # for i in range(10):
        #     print('%d) Reading %s/%s' % (i, bucket, key))
        #     try:
        #         payload = json.loads(read_from_s3(bucket, key))
        #         data = payload['data']
        #         break
        #     except Exception as e:
        #         print(e)
        #
        #     time.sleep(2)

        tmp_file = download_from_s3(bucket, key)
        #temp_file_names.append(tmp_file)

        gc.collect()

        with open(tmp_file, 'r') as fh:
            data = json.load(fh)['data']

        print('Read final data, reducing')

        if not final_data:
            final_data = data
        else:
            for ip, score in data.items():
                final_data.setdefault(ip, 0)
                final_data[ip] += float(score)

    print('Writing fiinal output data')
    write_to_s3(bucket, final_results_key, final_data)
