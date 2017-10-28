import pytest

from cupping.handlers.graphql import schema
from factories import (
        CuppingFactory,
        SessionFactory,
)

from pprint import pprint as pp

# Getting sessions

def test_get_all_sessions():
    SessionFactory.create_batch(3)
    query = '''
    query allSessions {
          sessions {
            id
            name
            formName
            created
          }
    }
    '''
    result = schema.execute(query)
    assert not result.errors
    sessions = result.data['sessions']
    assert len(sessions) == 3


def test_get_single_session():
    sessions = SessionFactory.create_batch(3)
    session = sessions[-1]
    query = """
    query allSessions($id: Int!) {
          sessions(id: $id) {
            id
            name
            formName
            created
          }
    }
    """
    result = schema.execute(query, variable_values={'id': session.id})
    assert not result.errors
    sessions = result.data['sessions']
    assert len(sessions) == 1
    assert sessions[0]['id'] == str(session.id)


def test_get_session_by_account_id():
    sessions = SessionFactory.create_batch(3, account_id=5)
    session = SessionFactory(account_id=888)
    query = """
    query allSessions($accountId: Int!) {
          sessions(accountId: $accountId) {
            id
            accountId
            cuppings {
                id
                name
                overallScore
            }
          }
    }
    """
    result = schema.execute(query, variable_values={'accountId': 888})
    assert not result.errors
    sessions = result.data['sessions']
    assert len(sessions) == 1
    s = sessions[0]
    assert s['id'] == str(session.id)
    assert s['accountId'] == 888


def test_get_invalid_session():
    query = """
    query allSessions($accountId: Int!) {
          sessions(accountId: $accountId) {
            id
            accountId
          }
    }
    """
    result = schema.execute(query, variable_values={'accountId': 888})
    assert not result.errors
    sessions = result.data['sessions']
    assert len(sessions) == 0


def test_get_all_sessions_with_cuppings():
    num_sessions = 3
    sessions = SessionFactory.create_batch(num_sessions)

    expected_cupping_lens = {}
    for i, session in enumerate(sessions):
        # create a variable number of cuppings per session, 3, 2, 1
        CuppingFactory.create_batch(num_sessions - i, session_id=session.id)
        expected_cupping_lens[session.id] = num_sessions - i

    query = """
    query allSessions($withCuppings: Boolean = true) {
          sessions {
            id
            name
            formName
            cuppings @include(if: $withCuppings) {
                id
                name
                scores
            }
          }
    }
    """
    result = schema.execute(query, variable_values={'withCuppings': True})
    assert not result.errors

    sessions = result.data['sessions']
    assert len(sessions) == 3

    for s in sessions:
        assert len(s['cuppings']) == expected_cupping_lens[int(s['id'])]


# Getting cuppings

def test_get_all_cuppings():
    session = SessionFactory()
    CuppingFactory.create_batch(3, session_id=session.id)
    query = """
    query allCuppings {
        cuppings {
            id
            name
            scores
        }
    }
    """
    result = schema.execute(query)
    assert not result.errors
    pp(result.data)



def test_query_cuppings_by_session_id():
    s = SessionFactory(account_id=12345)
    CuppingFactory.create_batch(3, session_id=s.id)

    # create a single session with a single cupping. This is the only thing which should be
    # returned from our query.
    session = SessionFactory(account_id=12345)
    cupping = CuppingFactory(session_id=session.id)
    # the query Cupping(param is jus tused to pass down the cuppings query below
    query = """
    query Cuppings($session_id: Int!) {
        cuppings(sessionId: $session_id) {
            id
            name
            scores
        }
    }
    """
    result = schema.execute(query, variable_values={'session_id': session.id})
    assert not result.errors
    pp(result.data)

    cuppings = result.data['cuppings']
    assert len(cuppings) == 1
    assert cuppings[0]['id'] == str(cupping.id)


# Create new session

def test_create_session(session_dict):
    pp(session_dict)
    query = """
    mutation SessionCreator {
        createSession (
            name: "GraphQL Test"
            formName: "GraphQL Form"
            accountId: "abc123"
        ) {
            ok
            session {
                id
                name
                formName
            }
        }
    }
    """
    result = schema.execute(query)
    pp(result.errors)
    pp(result.data)
