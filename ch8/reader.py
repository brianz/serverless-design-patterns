import boto3
import json
from datetime import datetime
import time
from pprint import pprint as pp
from base64 import b64decode

my_stream_name = 'bz-test'

kinesis = boto3.client('kinesis')

response = kinesis.describe_stream(StreamName=my_stream_name)

my_shard_id = response['StreamDescription']['Shards'][0]['ShardId']

shard_iterator = kinesis.get_shard_iterator(
        StreamName=my_stream_name,
        ShardId=my_shard_id,
        ShardIteratorType='LATEST')
        #ShardIteratorType='TRIM_HORIZON')

my_shard_iterator = shard_iterator['ShardIterator']
print('using', my_shard_iterator)


def decode_kinesis_data(response):
    records = [json.loads(record['Data'].decode()) for record in response['Records']]
    if len(records) == 1:
        records = records[0]
    print('records: %d' % (len(records), ))
    return records


response = kinesis.get_records(
        ShardIterator=my_shard_iterator,
        Limit=1,
)
pp(response)
print()
pp(decode_kinesis_data(response))


while 'NextShardIterator' in response:
    next_iterator = response.get('NextShardIterator')
    response = kinesis.get_records(
            ShardIterator=next_iterator,
            Limit=1,
    )

    decode_kinesis_data(response)

    time.sleep(2)
