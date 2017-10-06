from schematics.exceptions import DataError

from .decorators import decode_json
from .helpers import (
        create_session_from_json_payload,
        prettify_schematics_errors,
)

from ..models import (
        CuppingModel,
        SessionModel,
)
from ..persistence import Session, queries
from ..exceptions import Http404, InvalidInputData


@decode_json
def create_session(json_payload):
    if not json_payload or not hasattr(json_payload, 'get'):
        return {'errors': ['Invalid input data']}

    print('Creating session', json_payload)

    try:
        session = create_session_from_json_payload(json_payload)
        print('Created session: %s' % (session.id, ))
        response = {
                'session': {
                    'id': session.id,
                    'name': session.name,
                }
        }
    except InvalidInputData as e:
        response = {'errors': e.errors}

    return response


def get_session(data):
    print('Reading session', data)
    try:
        session_id = int(data.get('pathParameters', {}).get('id'))
    except (AttributeError, TypeError, ValueError):
        raise Http404('Invalid session id')

    session = queries.get_session_by_id(session_id)
    if session is None:
        raise Http404('Invalid session id')

    model = SessionModel.from_row(session)
    return {'session': model.to_native()}


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
