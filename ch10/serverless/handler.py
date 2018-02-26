import json
import sys

from pathlib import Path

CWD = Path(__file__).resolve().cwd() / 'lib'
sys.path.insert(0, str(CWD))

from raven import Client # Offical `raven` module
from raven_python_lambda import RavenLambdaWrapper


@RavenLambdaWrapper()
def hello(event, context):
    params = event.get('queryStringParameters', {})
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
