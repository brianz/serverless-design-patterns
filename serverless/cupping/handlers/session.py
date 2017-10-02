import json

from schematics.exceptions import DataError

from .helpers import prettify_schematics_errors

from ..models import (
        CuppingModel,
        SessionModel,
)
from ..persistence import Session
from ..exceptions import Http404


def decode_json(fn):
    def _decode_json_from_payload(payload):
        json_payload = json.loads(payload['body'])
        return fn(json_payload)
    return _decode_json_from_payload



@decode_json
def create_session(json_payload):
    print('Creating session', json_payload)

    cuppings = [{
            'scores': c.get('scores', {}),
            'overall_score': c.get('overallScore'),
            'defects': c.get('defects'),
            'descriptors': c.get('descriptors'),
            'notes': c.get('notes'),
            'is_sample': c.get('isSample'),
        } for c in json_payload.get('cuppings', ())]

    session_model = SessionModel({
        'name': json_payload.get('name'),
        'form_name': json_payload.get('formName'),
        'account_id': json_payload.get('accountId'),
        'user_id': json_payload.get('userId'),
        'cuppings': cuppings,
    })

    errors = ['Unknown error']
    response = {'errors': errors}

    try:
        session = Session.from_model(session_model)
        print('Created session: %s' % (session.id, ))
        return {
                'session': {
                    'id': session.id,
                    'name': session.name,
                }
        }
    except DataError as e:
        errors = prettify_schematics_errors(e)
    except Exception as e:
        errors = [str(e)]

    return {'errors': errors}


def get_session(data):
    print('Reading session', data)
    try:
        session_id = int(data.get('pathParameters', {}).get('id'))
    except ValueError:
        raise Http404('Invalid session id')



@decode_json
def update_session(json_payload):
    print('Updating session', json_payload)


def delete_session(data):
    print('Deleting session', data)


method_map = {
        'GET': get_session,
        'POST': create_session,
        'PUT': update_session,
        'DELETE': delete_session,
}


def handle_session(http_method, payload):
    method = http_method.upper()
    return method_map[method](payload)
