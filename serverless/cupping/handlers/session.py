import json

from ..models import (
        Cupping,
        Session,
)


def decode_json(fn):
    def _decode_json_from_payload(payload):
        json_payload = json.loads(payload['body'])
        return fn(json_payload)
    return _decode_json_from_payload


@decode_json
def create_session(json_payload):
    print('Creating session', json_payload)
    session = Session.create(json_payload)
    print('Created session: %s' % (session.id, ))
    return {
            'session': {
                'id': session.id,
                'name': session.name,
            }
    }


def read_session(data):
    print('Reading session', data)


@decode_json
def update_session(json_payload):
    print('Updating session', json_payload)


def delete_session(data):
    print('Deleting session', data)


method_map = {
        'GET': create_session,
        'POST': create_session,
        'PUT': create_session,
        'DELETE': create_session,
}


def handle_session(http_method, payload):
    method = http_method.upper()
    return method_map[method](payload)
