import boto3

_clients = {}


def _get_client(service):
    global _clients
    client = _clients.get(service)
    if not client:
        client = boto3.client(service)
        _clients[service] = client

    return client


def read_from_s3(bucket, key):
    client = _get_client('s3')
    return client.get_object(Bucket=bucket, Key=key)


def read_body_from_s3(bucket, key):
    obj = read_from_s3(bucket, key)
    return obj['Body'].read()


def write_to_s3(bucket, key, payload, **kwargs):
    client = _get_client('s3')
    return client.put_object(
            Body=payload.encode(),
            Bucket=bucket,
            Key=key,
            **kwargs,
    )


def list_s3_bucket(name, prefix=None, suffix=None):
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(name=name)
    results = bucket.objects.filter(Prefix=prefix)
    return [(r.bucket_name, r.key) for r in results]
