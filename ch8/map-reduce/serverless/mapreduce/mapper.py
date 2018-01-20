import json
import csv
import os
import uuid

from .aws import (
        download_from_s3,
        invoke_lambda,
        list_s3_bucket,
        publish_to_sns,
        write_to_s3,
)

from pprint import pprint as pp

IP = 'ip'
DESTINATION_URL = 'url'
VISIT_DATA = 'vd'
AD_REVENUE = 'rev'
USER_AGENT = 'ua'
COUNTRY_CODE = 'cc'
LANGUAGE_CODE = 'lc'
SEARCH_WORD = 'sw'
DURATION = 'dur'

USER_VISIT_FIELD_NAMES = (
        IP,
        DESTINATION_URL,
        VISIT_DATA,
        AD_REVENUE,
        USER_AGENT,
        COUNTRY_CODE,
        LANGUAGE_CODE,
        SEARCH_WORD,
        DURATION,
)


def _csv_lines_from_filepath(filepath, delete=True):
    with open(filepath, 'rt') as fh:
        reader = csv.DictReader(fh, USER_VISIT_FIELD_NAMES)
        for row in reader:
            yield row

    if delete:
        os.remove(filepath)


def _invoke_reducer(payload):
    #invoke_lambda('map-reduce-dev-Reducer', payload)
    bucket = 'brianz-dev-mapreduce-results'

    job_id = payload['job_id']
    run_id = payload['run_id']
    batch = payload['batch']
    data = payload['data']

    if not data:
        print('Error, empty data')
        return

    key = 'run-%s/job-%s-payload-%s.json' % (run_id, job_id, batch)
    write_to_s3(bucket, key, payload)


def crawl(bucket_name, prefix='pavlo/text/tiny/uservisits/part-'):
    """Entrypoint for a map-reduce job.

    The function is responsible for crawling a particular S3 bucket and publishing map jobs
    asyncrhonously using SNS where the mapping is 1-to-1, file-to-sns.

    It's presumed that lambda mapper functions are hooked up to the SNS topic. These Lambda mappers
    will each work on a particular file.

    """
    # Unique identifer for the entire map-reduce run
    run_id = str(uuid.uuid4())
    mapper_data = [
            {
                'bucket': bucket,
                'job_id': str(uuid.uuid4()),
                'key': key,
                'run_id': run_id,
            } for (bucket, key) in list_s3_bucket(bucket_name, prefix)
    ]

    # Let's add in the total number of jobs which will be kicked off. Note that the mappers
    # themselves will break up their work into chunks so as not to send too much data to each
    # reducer.
    num_mappers = len(mapper_data)

    for mapper_dict in mapper_data:
        mapper_dict['total_jobs'] = num_mappers
        publish_to_sns(mapper_dict)


def map(event):
    message = json.loads(event['Records'][0]['Sns']['Message'])

    total_jobs = message['total_jobs']
    run_id = message['run_id']
    job_id = message['job_id']

    tmp_file = download_from_s3(message['bucket'], message['key'])

    ad_revenue_by_ip = {}
    line_number = 0
    batch = 0
    bucket = 'brianz-dev-mapreduce-results'

    for line in _csv_lines_from_filepath(tmp_file):
        ip = line['ip']
        ad_revenue_by_ip.setdefault(ip, 0)
        ad_revenue_by_ip[ip] += float(line[AD_REVENUE])

        # Send off a mapper job every 10,000 lines
        line_number += 1
        if line_number >= 10000:
            payload = {
                    'batch': batch,
                    'job_id': job_id,
                    'data': ad_revenue_by_ip,
                    'run_id': run_id,
            }
            _invoke_reducer(payload)

            ad_revenue_by_ip = {}
            batch += 1
            line_number = 0


    # get off anything remaining
    if ad_revenue_by_ip:
        payload = {
                'batch': batch,
                'job_id': job_id,
                'data': ad_revenue_by_ip,
                'run_id': run_id,
        }
        _invoke_reducer(payload)


    invoke_data = {
        'batches': batch + 1,
        'bucket': bucket,
        'job_id': job_id,
        'run_id': run_id,
        'total_jobs': total_jobs,
    }

    invoke_lambda('map-reduce-dev-BatchReducer', invoke_data, invocation_type='RequestResponse')

    # Writing this signals that the batch is all done and that the batch reducer can start
    # key = 'run-%s/job-%s-batch-done.json' % (run_id, job_id, )
    # write_to_s3(bucket, key, {
    #     'batches': batch + 1,
    #     'job_id': job_id,
    #     'run_id': run_id,
    #     'total_jobs': total_jobs,
    # })
