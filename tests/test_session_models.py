from decimal import Decimal

from cupping.db import dbtransaction, commit_session, get_session
from cupping.models import Session



def test_session_create_no_cuppings():
    s = Session.create({
            'name': 'Test Session',
            'formName': 'SCAA'
    })
    assert s.id
    assert s.name == 'Test Session'
    assert s.form_name == 'SCAA'
    assert s.cuppings == []


def test_session_create_cuppings():
    s = Session.create({
            'name': 'Test Session',
            'formName': 'SCAA',
            'cuppings': [
                {
                    'scores': {'Aroma': 8, 'Flavor': 6},
                    'overallScore': 88.8,
                },
                {
                    'scores': {'Aroma': 6, 'Flavor': 7},
                    'overallScore': 75,
                },
            ]
    })
    assert s.id

    expected_overall = sorted([Decimal('88.8'), Decimal('75')])
    actual_overall = sorted([c.total_score for c in s.cuppings])
    assert expected_overall == actual_overall
