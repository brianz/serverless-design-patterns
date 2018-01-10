import boto3
import json
import sys
import csv
import codecs
import io
import tempfile
import os

from pathlib import Path

# Munge our sys path so libs can be found
CWD = Path(__file__).resolve().cwd() / 'lib'
sys.path.insert(0, str(CWD))



def read_file_from_s3(bucket_name, key):
    client = boto3.client('s3')
    obj = client.get_object(Bucket=bucket_name, Key=key)
    return obj['Body']
    #return obj['Body'].read()
    #return json.loads(obj['Body'].read())


def download_from_s3(bucket_name, key):
    client = boto3.resource('s3')
    #(fd, fn) = tempfile.mkstemp(suffix='.txt', prefix='aws-', text=True)
    tmp = tempfile.NamedTemporaryFile(
            mode='w+t',
            #buffering=None,
            #encoding=None,
            prefix='aws-',
            dir='/tmp',
            delete=False)
    tmp.close()
    #fn = '/tmp/part-00000'
    client.Bucket(bucket_name).download_file(key, tmp.name)
    #return (fd, fn)
    return tmp


def s3_body_to_iter(body):
    chunk_size = 4096
    # body = StreamingBodyIO(body)
    # return io.BufferedReader(body)
    for chunk in iter(lambda: body.read(chunk_size), b''):
        lines = chunk.split('\n')
        yield str(chunk)


def mapper(event, context):
    #bucket = 's3://big-data-benchmark/pavlo/text/tiny/uservisits/'
    bucket_name = 'big-data-benchmark'

    key = 'pavlo/text/tiny/uservisits/part-00000'
    #key = 'pavlo/text/1node/uservisits/part-00000'

    num_rows = 0
    row = None

    # # code for reading into memory and iterating
    # data = read_file_from_s3(bucket_name, key)
    # data = io.StringIO(data.read().decode('utf-8'))
    # reader = csv.reader(data)
    # for row in reader:
    #     num_rows += 1


    # code for downloading to disk, opening and then iterating
    fh = download_from_s3(bucket_name, key)
    fn = fh.name
    print(fn)

    try:
        with open(fn, 'rt') as fh:
            reader = csv.reader(fh)
            for row in reader:
                num_rows += 1

            print(row)
            print(num_rows)
    finally:
        fh.close()
