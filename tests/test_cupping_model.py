import pytest

from decimal import Decimal

from cupping.db import dbtransaction, commit_session, get_session
from cupping.models import Cupping, Session


@pytest.fixture()
def session():
    return Session.create({
        'name': 'test session',
        'formName': 'scaa',
    })


def test_cupping_create(session):
    scores = {'Aroma': 8, 'Flavor': 6.5}
    data = {
            'scores': scores,
            'overallScore': 88.5,
            # note leading/trailing spaces should be stripped
            'descriptors': [' berry ', 'fruit'],
            'defects': [' sour ', 123],
            'notes': 'This was really good',
            'isSample': 'true',
    }
    c = Cupping.create(data, session=session)
    commit_session()

    assert c.id
    assert c.session_id == session.id
    assert c.scores == scores
    assert c.overall_score == Decimal('88.5')
    assert c.descriptors == ['berry', 'fruit']
    assert c.defects == ['sour', '123']
    assert c.notes == 'This was really good'
    assert c.is_sample == True

    # Test the forward relationship
    assert c.session.id == session.id


def test_cupping_create_default_values(session):
    scores = {'Aroma': 8, 'Flavor': 6.5}
    data = {
            'scores': scores,
            'overallScore': 88.5,
    }
    c = Cupping.create(data, session=session)
    commit_session()
    assert c.defects == []
    assert c.descriptors == []
    assert c.is_sample == False


def test_cupping_create_scores_requires_dict(session):
    scores = [{'Aroma': 8, 'Flavor': 6.5}]
    data = {
            'scores': scores,
            'overallScore': 88.5,
    }
    with pytest.raises(ValueError) as e:
        Cupping.create(data, session=session)

    assert 'Scores must be a mapping of name to numeric value' in str(e)


def test_cupping_create_descriptors_requires_list(session):
    scores = {'Aroma': 8, 'Flavor': 6.5}
    data = {
            'scores': scores,
            'overallScore': 88.5,
            'descriptors': 'yummy',
    }
    with pytest.raises(ValueError) as e:
        Cupping.create(data, session=session)

    assert 'descriptors must be a list of strings' in str(e)


def test_cupping_create_defects_requires_list(session):
    scores = {'Aroma': 8, 'Flavor': 6.5}
    data = {
            'scores': scores,
            'overallScore': 88.5,
            'defects': 'yummy',
    }
    with pytest.raises(ValueError) as e:
        Cupping.create(data, session=session)

    assert 'defects must be a list of strings' in str(e)


