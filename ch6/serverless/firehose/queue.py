import boto3
import json
import os
import urllib2


TWITTER_STREAM_QUEUE_NAME = os.environ['TWITTER_STREAM_QUEUE_NAME']

_sqs_client = None
_s3_client = None
_sqs_url = None


def get_sqs_client():
    global _sqs_client
    if _sqs_client is None:
        _sqs_client = boto3.client('sqs')
    return _sqs_client


def get_queue_url():
    global _sqs_url
    if _sqs_url is None:
        client = get_sqs_client()
        response = client.get_queue_url(QueueName=TWITTER_STREAM_QUEUE_NAME)
        _sqs_url = response['QueueUrl']
    return _sqs_url


def publish_tweet(payload):
    msg = json.dumps(payload)
    client = get_sqs_client()
    sqs_url = get_queue_url()

    return client.send_message(
                QueueUrl=sqs_url,
                MessageBody=msg)


def classify_photos():
    rekognition = boto3.client('rekognition')
    sqs = get_sqs_client()
    sqs_url = get_queue_url()

    should_continue = True

    while should_continue:
        response = sqs.receive_message(
            QueueUrl=sqs_url,
            MaxNumberOfMessages=10,
        )
        messages = response.get('Messages', [])
        if not messages:
            should_continue = False

        for msg in messages:
            receipt = msg['ReceiptHandle']
            body = json.loads(msg['Body'])

            text = body['text']
            url = body['url']

            image_response = urllib2.urlopen(url)
            results = rekognition.detect_labels(Image={'Bytes': image_response.read()})
            print url, results['Labels']

            sqs.delete_message(QueueUrl=sqs_url, ReceiptHandle=receipt)
