from .aws import (
        write_to_s3,
)

# def write_to_s3(payload):
#     json_payload = json.dumps(payload, indent=2)
#     fh = io.StringIO(json_payload)
#     client = boto3.client('s3')
#     response = client.put_object(
#             body=fh,
#             bucket=RESULTS_BUCKET,
# )


import uuid

def reduce(event):
    bucket = 'brianz-dev-mapreduce-results'
    key = str(uuid.uuid4())
    write_to_s3(bucket, key, event)
