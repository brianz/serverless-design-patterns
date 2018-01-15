import json
import csv
import os

from .aws import (
        download_from_s3,
        invoke_lambda,
        list_s3_bucket,
        publish_to_sns,
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

def csv_lines_from_filepath(filepath, delete=True):
    with open(filepath, 'rt') as fh:
        reader = csv.DictReader(fh, USER_VISIT_FIELD_NAMES)
        for row in reader:
            yield row

    if delete:
        os.remove(filepath)


def crawl(bucket_name, prefix='pavlo/text/tiny/uservisits/part-'):
    mapper_data = [
            {'bucket': bucket, 'key': key} \
            for (bucket, key) in list_s3_bucket(bucket_name, prefix)
    ]
    num_mappers = len(mapper_data)
    for mapper_dict in mapper_data:
        mapper_dict['total_jobs'] = num_mappers
        publish_to_sns(mapper_dict)



def map(event):
    payload = json.loads(event['Records'][0]['Sns']['Message'])
    total_jobs = payload['total_jobs']

    tmp_file = download_from_s3(payload['bucket'], payload['key'])

    ad_revenue_by_ip = {}
    line_number = 0
    total_invocations = 0
    for line in csv_lines_from_filepath(tmp_file):
        ip = line['ip']
        ad_revenue_by_ip.setdefault(ip, 0)
        ad_revenue_by_ip[ip] += float(line[AD_REVENUE])

        line_number += 1
        if line_number >= 10000:
            invoke_lambda(ad_revenue_by_ip)
            line_number = 0
            ad_revenue_by_ip = {}
            total_invocations += 1

    # get off anything remaining
    if ad_revenue_by_ip:
        invoke_lambda(ad_revenue_by_ip)
        total_invocations += 1

    print('Total invocations:', total_invocations)
