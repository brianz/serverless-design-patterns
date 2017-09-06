import pytest

from decimal import Decimal
from schematics.exceptions import DataError

from helpers import prettify_schematics_errors


def test_session_create_name_required(session):
    session.form_name = 'my form'

    with pytest.raises(DataError) as e:
        session.validate()

    errors = prettify_schematics_errors(e)
    assert errors == {
            'name': ['This field is required.'],
    }


def test_session_create_form_name_required(session):
    session.name = 'Test cupping'

    with pytest.raises(DataError) as e:
        session.validate()

    errors = prettify_schematics_errors(e)
    assert errors == {
            'form_name': ['This field is required.'],
    }


def test_session_create_account_id_requires_int(valid_session):
    valid_session.account_id = 'a123'

    with pytest.raises(DataError) as e:
        valid_session.validate()

    errors = prettify_schematics_errors(e)
    assert errors == {
            'account_id': ["Value 'a123' is not int."],
    }


def test_session_create_user_id_requires_int(valid_session):
    valid_session.user_id = 'a123'

    with pytest.raises(DataError) as e:
        valid_session.validate()

    errors = prettify_schematics_errors(e)
    assert errors == {
            'user_id': ["Value 'a123' is not int."],
    }


def test_session_valid_no_cuppings(valid_session):
    assert not valid_session.validate()
    assert not valid_session.cuppings


def test_session_valid_cuppings(valid_session, cuppings):
    valid_session.cuppings = cuppings
    assert not valid_session.validate()

    for c in valid_session.cuppings:
        for value in c.scores.values():
            assert isinstance(value, Decimal)
