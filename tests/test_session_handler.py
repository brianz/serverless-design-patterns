import json
import pytest

from factories import SessionFactory, CuppingFactory

from cupping.exceptions import Http404
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

def test_get_session():
    session = SessionFactory()
    cuppings = CuppingFactory.create_batch(2, session_id=session.id)

    response = get_session({'pathParameters': {'id': session.id}})

    return_session =  response.get('session')
    assert return_session
    assert return_session['id'] == session.id
    assert len(return_session['cuppings']) == 2

    session_ids = set(c['session_id'] for c in return_session['cuppings'])
    assert session_ids == set((session.id, ))


def test_get_nonexistent_session():
    with pytest.raises(Http404) as e:
        get_session({'pathParameters': {'id': 23423423}})
    assert 'Invalid session id' in str(e)


_invalid_session_ids = (None, 'abc', [], 0, ('123',))

@pytest.mark.parametrize('session_id', _invalid_session_ids)
def test_get_invalid_session(session_id):
    with pytest.raises(Http404) as e:
        get_session({'pathParameters': {'id': session_id}})
    assert 'Invalid session id' in str(e)


_invalid_data = ({}, [], None, '', {'foo': 123}, {'pathParameters': None})

@pytest.mark.parametrize('data', _invalid_data)
def test_get_bad_data(data):
    with pytest.raises(Http404) as e:
        get_session(data)
    assert 'Invalid session id' in str(e)



