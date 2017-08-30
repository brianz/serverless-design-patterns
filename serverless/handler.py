import json
import sys

from pathlib import Path

# Munge our sys path so libs can be found
CWD = Path(__file__).resolve().cwd() / 'lib'
sys.path.insert(0, str(CWD))

from cupping.handlers.session import handle_session
from cupping.db import setup_db


def session(event, context):
    setup_db()
    http_method = event['httpMethod']
    response = handle_session(http_method, event)

    body = {
        "message": "Go Serverless v1.0! Your function executed successfully!",
        "input": event
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response
