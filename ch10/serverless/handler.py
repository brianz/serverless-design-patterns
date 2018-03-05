import json
import os
import sys

from pathlib import Path

CWD = Path(__file__).resolve().cwd() / 'lib'
sys.path.insert(0, str(CWD))

from raven_python_lambda import RavenLambdaWrapper



@RavenLambdaWrapper()
def divide(event, context):
    params = event.get('queryStringParameters') or {}
    numerator = int(params.get('numerator', 10))
    denominator = int(params.get('denominator', 2))
    body = {
        "message": "Results of %s / %s = %s" % (
            numerator,
            denominator,
            numerator // denominator,
        )
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response


state_variable = None

def process(event, context):
    global state_variable

    if not state_variable:
        print("Initializging state_variable")
        state_variable = 0

    state_variable += 1
    return {
        'statusCode': 200,
        'body': json.dumps({'state_variable': state_variable}),
    }
