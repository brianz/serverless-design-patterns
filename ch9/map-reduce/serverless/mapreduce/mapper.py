import json
import csv
import os
import time
import uuid

from ipaddress import IPv4Address

from .aws import (
        download_from_s3,
        invoke_lambda,
        list_s3_bucket,
        publish_to_sns,
        write_to_s3,
        write_csv_to_s3,
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


def crawl(bucket_name, prefix='pavlo/text/tiny/uservisits/part-'):
    """Entrypoint for a map-reduce job.

    The function is responsible for crawling a particular S3 bucket and publishing map jobs
    asyncrhonously using SNS where the mapping is 1-to-1, file-to-sns.

    It's presumed that lambda mapper functions are hooked up to the SNS topic. These Lambda mappers
    will each work on a particular file.

    """
    print('Starting at: %s: %s' % (time.time(), time.asctime(), ))
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

    # Let's add in the total number of jobs which will be kicked off.
    num_mappers = len(mapper_data)

    for i, mapper_dict in enumerate(mapper_data):
        mapper_dict['total_jobs'] = num_mappers
        mapper_dict['job_id'] = i
        publish_to_sns(mapper_dict)


def map(event):
    message = json.loads(event['Records'][0]['Sns']['Message'])

    total_jobs = message['total_jobs']
    run_id = message['run_id']
    job_id = message['job_id']

    tmp_file = download_from_s3(message['bucket'], message['key'])

    ad_revenue_by_ip = {}
    line_number = 0
    bucket = 'brianz-dev-mapreduce-results'

    for line in _csv_lines_from_filepath(tmp_file):
        ip = int(IPv4Address(line['ip']))
        if ip in ad_revenue_by_ip:
            ad_revenue_by_ip[ip] += float(line[AD_REVENUE])
        else:
            ad_revenue_by_ip[ip] = float(line[AD_REVENUE])

    if not ad_revenue_by_ip:
        return

    metadata = {
            'job_id': str(job_id),
            'run_id': str(run_id),
            'total_jobs': str(total_jobs),
    }

    key = 'run-%s/mapper-%s-final-done.csv' % (run_id, job_id)
    write_csv_to_s3(bucket, key, ad_revenue_by_ip, Metadata=metadata)
