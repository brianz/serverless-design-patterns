import json
import pytest

from cupping.handlers.session import (
        create_session,
        get_session,
        update_session,
        delete_session,
)


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
    payload = {'body': json.dumps(payload)}
    response = create_session(payload)
    assert response['session']
    assert response['session']['name'] == 'Test cupping'
    assert response['session']['id'] >= 1



_invalid_inputs = ('None', '0', 'stringy', '{}', '', '[]', '["abc"]', 'false')

@pytest.mark.parametrize('data', _invalid_inputs)
def test_create_session_invalid_data(data):
    response = create_session({'body': data})
    assert response == {'errors': 'Invalid input data'}


def test_unhandled_exception(mocker, payload):
    m_model = mocker.patch('cupping.handlers.session.create_session_from_json_payload')
    m_model.side_effect = Exception('Ooops')
    payload = {'body': json.dumps(payload)}
    response = create_session(payload)
    assert response == {'errors': ['Ooops']}


def test_create_session_no_cuppings(payload):
    payload.pop('cuppings')
    payload = {'body': json.dumps(payload)}
    response = create_session(payload)
    assert response['session']
    assert response['session']['name'] == 'Test cupping'
    assert response['session']['id'] >= 1


def test_create_session_missing_name(payload):
    payload.pop('name')
    payload = {'body': json.dumps(payload)}
    response = create_session(payload)
    assert response == {'errors': {'name': 'This field is required.'}}


def test_create_session_missing_cupping_scores(payload):
    payload['cuppings'][0].pop('scores')
    payload = {'body': json.dumps(payload)}
    response = create_session(payload)
    assert response == {
        'errors': {
            'cuppings': {
                0: {'scores': 'This field is required.'}
            }
        }
    }


# GET session

from factories import SessionFactory

def test_get_session():
    session = SessionFactory()
    response = get_session({'pathParameters': {'id': session.id}})

    assert response == {
        'session': {
            'id': session.id,
            'name': session.name,
        }
    }
