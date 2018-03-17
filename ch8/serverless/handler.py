import boto3
import sys
import os

from datetime import datetime
from pathlib import Path
import json

CWD = Path(__file__).resolve().cwd() / 'lib'
sys.path.insert(0, str(CWD))

from pprint import pprint as pp
from lambda_arch.aws import read_body_from_s3, write_to_s3


def hello(event, context):
    record = event['Records'][0]
    s3 = record['s3']
    bucket = s3['bucket']['name']
    key = s3['object']['key']

    data = read_body_from_s3(bucket, key).decode()

    product_prices = {}

    lines = [json.loads(l) for l in data.split('|||') if l]
    times = []

    for line in lines:
        if line.get('side') != 'buy':
            continue

        product_id = line['product_id']
        price = float(line['price'])

        times.append(line['time'])
        if product_id not in product_prices:
            product_prices[product_id] = {'prices': [price]}
        else:
            product_prices[product_id]['prices'].append(price)

    if not product_prices:
        return

    times.sort()
    latest_time = times[-1]
    DT_FORMAT = '%Y-%m-%dT%H:%M:%S.%fZ'
    latest_dt = datetime.strptime(latest_time, DT_FORMAT)

    new_key = latest_dt.strftime('%Y/%m/%d/%H/%M.json')

    for key in product_prices:
        prices = product_prices[key]['prices']
        average_price = sum(prices) * 1.0 / len(prices)
        product_prices[key]['average'] = average_price

    new_payload = json.dumps(product_prices, indent=2)

    destination_bucket = os.environ['DESTINATION_BUCKET']
    print('Uploading to', destination_bucket, new_key)
    write_to_s3(destination_bucket, new_key, new_payload)
