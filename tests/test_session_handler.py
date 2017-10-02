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
            'isSammple': False,
        },
        {
            'scores': {'Aroma': 5.6, 'Flavor': 8.4},
            'overallScore': 85,
            'defects': [],
            'descriptors': [],
            'notes': '',
            'isSammple': False,
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


def test_create_session(payload):
    payload = {'body': json.dumps(payload)}
    response = create_session(payload)
    assert response['session']
    assert response['session']['name'] == 'Test cupping'
    assert response['session']['id'] >= 1


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
    payload['cuppings'][0]['scores'] = []
    payload = {'body': json.dumps(payload)}
    response = create_session(payload)
    assert response == {
        'errors': {
            'cuppings': {
                0: {'scores': 'Only mappings may be used in a DictType'}
            }
        }
    }
