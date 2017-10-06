import json
import pytest

from factories import SessionFactory, CuppingFactory

from cupping.exceptions import Http404

import handler

from helpers import (
        assert_200,
        assert_404,
        assert_500,
        get_body_from_response,
)


def create_session(payload):
    if not isinstance(payload, str):
        payload = json.dumps(payload)
    event = {'httpMethod': 'POST', 'body': payload}
    return handler.session(event, None)


def get_session(payload):
    if isinstance(payload, dict):
        payload['httpMethod'] = 'GET'
        event = payload
    else:
        event = {'httpMethod': 'GET', 'pathParameters': payload}

    return handler.session(event, None)


@pytest.fixture()
def cuppings():
    return [
        {
            'scores': {'Aroma': 8.6, 'Flavor': 5.5},
            'overallScore': 75,
            'defects': ['stank', 'pu'],
            'descriptors': ['honey', 'berry', 'mungy'],
            'notes': 'Pretty good with elements of stank',
            'isSample': False,
        },
        {
            'scores': {'Aroma': 5.6, 'Flavor': 8.4},
            'overallScore': 85,
            'defects': [],
            'descriptors': [],
            'notes': '',
            'isSample': False,
        },
    ]


@pytest.fixture()
def payload(cuppings):
    return {
        'name': 'Test cupping',
        'formName': 'SCAA',
        'accountId': 123,
        'userId': 456,
        'cuppings': cuppings,
    }


# POST session

def test_create_session(payload):
    response = create_session(payload)
    assert_200(response)
    body = get_body_from_response(response)
    assert body['session']
    assert body['session']['name'] == 'Test cupping'
    assert body['session']['id'] >= 1



_invalid_inputs = (None, 0, 'stringy', {}, '', [], ["abc"], False)

@pytest.mark.parametrize('data', _invalid_inputs)
def test_create_session_invalid_data(data):
    response = create_session(data)
    assert_200(response)
    body = get_body_from_response(response)
    assert body == {'errors': ['Invalid input data']}


def test_unhandled_exception(mocker, payload):
    m_handler = mocker.patch.object(handler, 'handle_session')
    m_handler.side_effect = Exception('Ooops')
    response = create_session(payload)
    assert_500(response)
    body = get_body_from_response(response)
    assert body == {'errors': ['Unexpected server error']}


def test_deep_unhandled_exception(mocker, payload):
    m_model = mocker.patch('cupping.handlers.session.create_session_from_json_payload')
    m_model.side_effect = Exception('Ooops')
    response = create_session(payload)
    assert_500(response)
    body = get_body_from_response(response)
    assert body == {'errors': ['Unexpected server error']}


def test_create_session_no_cuppings(payload):
    payload.pop('cuppings')
    response = create_session(payload)
    assert_200(response)
    body = get_body_from_response(response)
    assert body['session']
    assert body['session']['name'] == 'Test cupping'
    assert body['session']['id'] >= 1


def test_create_session_missing_name(payload):
    payload.pop('name')
    response = create_session(payload)
    assert_200(response)
    body = get_body_from_response(response)
    assert body == {'errors': {'name': 'This field is required.'}}


def test_create_session_missing_cupping_scores(payload):
    payload['cuppings'][0].pop('scores')
    response = create_session(payload)
    assert_200(response)
    body = get_body_from_response(response)
    assert body == {
        'errors': {
            'cuppings': {
                '0': {'scores': 'This field is required.'}
            }
        }
    }


# GET session

def test_get_session():
    session = SessionFactory()
    cuppings = CuppingFactory.create_batch(2, session_id=session.id)

    response = get_session({'pathParameters': {'id': session.id}})
    assert_200(response)
    body = get_body_from_response(response)

    return_session =  body.get('session')
    assert return_session
    assert return_session['id'] == session.id
    assert len(return_session['cuppings']) == 2

    session_ids = set(c['session_id'] for c in return_session['cuppings'])
    assert session_ids == set((session.id, ))


@pytest.fixture
def invalid_session_response():
    return {'errors': ['Invalid session id']}


def test_get_nonexistent_session(invalid_session_response):
    payload = {'pathParameters': {'id': 23423423}}
    response = get_session(payload)
    assert response['statusCode'] == 404
    body = get_body_from_response(response)
    assert body == invalid_session_response


_invalid_session_ids = (None, 'abc', [], 0, ('123',))

@pytest.mark.parametrize('session_id', _invalid_session_ids)
def test_get_invalid_session(session_id, invalid_session_response):
    payload = {'pathParameters': {'id': session_id}}
    response = get_session(payload)
    assert response['statusCode'] == 404
    body = get_body_from_response(response)
    assert body == invalid_session_response


_invalid_data = ({}, [], None, '', {'foo': 123}, {'pathParameters': None})

@pytest.mark.parametrize('data', _invalid_data)
def test_get_bad_data(data, invalid_session_response):
    response = get_session(data)
    assert response['statusCode'] == 404
    body = get_body_from_response(response)
    assert body == invalid_session_response
