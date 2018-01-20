import boto3
import botocore
import csv
import io
import json
import tempfile

from .constants import SNS_MAPPER_ARN

_clients = {}


def _get_client(service):
    global _clients
    client = _clients.get(service)
    if not client:
        client = boto3.client(service)
        _clients[service] = client

    return client



def invoke_lambda(name, payload, invocation_type='Event'):
    client = _get_client('lambda')
    payload = bytes(json.dumps(payload), 'utf-8')
    response = client.invoke(
        FunctionName=name,
        InvocationType=invocation_type,
        Payload=payload,
    )


def publish_to_sns(payload):
    client = _get_client('sns')
    client.publish(
            TargetArn=SNS_MAPPER_ARN,
            Message=json.dumps({'default': json.dumps(payload)}),
            MessageStructure='json',
    )


def download_from_s3(bucket_name, key, s3=None):
    s3 = s3 or boto3.resource('s3')
    tmp = tempfile.NamedTemporaryFile(
            mode='w+t',
            prefix='aws-',
            dir='/tmp',
            delete=False)
    tmp.close()
    s3.Bucket(bucket_name).download_file(key, tmp.name)
    return tmp.name


def s3_file_exists(bucket_name, key):
    s3 = boto3.resource('s3')

    try:
        s3.Object(bucket_name, key).load()
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            return False
        else:
            print(e.response)
            return False

    return True


def read_from_s3(bucket_name, key):
    client = _get_client('s3')
    obj = client.get_object(Bucket=bucket_name, Key=key)
    return obj['Body'].read()


def write_to_s3(bucket, key, payload):
    json_payload = json.dumps(payload, indent=2)
    body = bytes(json_payload, 'utf-8')

    client = boto3.client('s3')
    response = client.put_object(
            Body=body,
            Bucket=bucket,
            Key=key,
    )


def list_s3_bucket(name, prefix=None, suffix=None):
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(name=name)
    results = bucket.objects.filter(Prefix=prefix)
    return [(r.bucket_name, r.key) for r in results]
