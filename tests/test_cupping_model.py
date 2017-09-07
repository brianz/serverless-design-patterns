import pytest

from decimal import Decimal
from schematics.exceptions import DataError

from helpers import prettify_schematics_errors

from cupping.models import CuppingModel


def test_session_invalid_cupping_score():
    with pytest.raises(DataError) as e:
        CuppingModel({
            'session_id': 10,
            'scores': {
                'Aroma': 'abc',
                'Flavor': '5',
            },
            'overall_score': 88.5,
        })

    errors = prettify_schematics_errors(e)
    assert errors == {
           'scores': {
               'Aroma': ["Number 'abc' failed to convert to a decimal."]
            }
    }


def test_session_overall_score_min_value():
    c = CuppingModel({
        'session_id': 10,
        'scores': {},
        'overall_score': '-0.1',
    })
    with pytest.raises(DataError) as e:
        c.validate()

    errors = prettify_schematics_errors(e)
    assert errors == {
           'overall_score': ['Value should be greater than or equal to 0.']
    }


def test_session_overall_score_max_value():
    c = CuppingModel({
        'session_id': 10,
        'scores': {},
        'overall_score': '100.1',
    })
    with pytest.raises(DataError) as e:
        c.validate()

    errors = prettify_schematics_errors(e)
    assert errors == {
           'overall_score': ['Value should be less than or equal to 100.']
    }


def test_session_scores_required():
    c = CuppingModel({
        'session_id': 10,
        'overall_score': '100',
    })
    with pytest.raises(DataError) as e:
        c.validate()

    errors = prettify_schematics_errors(e)
    assert errors == {
           'scores': ['This field is required.']
    }


def test_session_invalid_overall_score():
    with pytest.raises(DataError) as e:
        CuppingModel({
            'session_id': 10,
            'overall_score': 'abc',
        })

    errors = prettify_schematics_errors(e)
    assert errors == {
           'overall_score': ["Number 'abc' failed to convert to a decimal."]
    }
