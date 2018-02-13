import csv
import itertools
import json
import os
import sys
import time
import uuid

import email.parser

# Make sure we can read big csv files
csv.field_size_limit(sys.maxsize)

from .aws import (
        download_from_s3,
        invoke_lambda,
        list_s3_bucket,
        publish_to_sns,
        read_body_from_s3,
        write_to_s3,
        write_csv_to_s3,
)

from pprint import pprint as pp


def _csv_lines_from_filepath(filepath, delete=True):
    with open(filepath, 'rt') as fh:
        reader = csv.DictReader(fh, fieldnames=('file', 'message'))
        for row in reader:
            yield row

    if delete:
        os.remove(filepath)


def crawl(bucket_name, prefix=''):
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

    counts = {}

    bucket = 'brianz-dev-mapreduce-results'

    tmp_file = download_from_s3(message['bucket'], message['key'])

    parser = email.parser.Parser()

    for line in _csv_lines_from_filepath(tmp_file):
        msg = line['message']
        eml = parser.parsestr(msg, headersonly=True)
        _from = eml['From']
        _tos = eml.get('To')

        if not _tos:
            continue

        _tos = (t.strip() for t in _tos.split(','))

        for from_to in itertools.product([_from], _tos):
            if from_to not in counts:
                counts[from_to] = 1
            else:
                counts[from_to] += 1

    if not counts:
        return

    metadata = {
            'job_id': str(job_id),
            'run_id': str(run_id),
            'total_jobs': str(total_jobs),
    }

    key = 'run-%s/mapper-%s-done.csv' % (run_id, job_id)
    write_csv_to_s3(bucket, key, counts, Metadata=metadata)
