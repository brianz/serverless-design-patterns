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
        'body': json.dumps({
            'name': 'Test cupping',
            'formName': 'SCAA',
            'accountId': 123,
            'userId': 456,
            'cuppings': cuppings,
        })
    }


def test_create_session(payload):
    from pprint import pprint as pp
    #pp(payload)
    response = create_session(payload)
    pp(response)
