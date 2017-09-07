import pytest

from decimal import Decimal

from cupping.db import (
        dbtransaction,
        commit_session,
        get_session,
)
from cupping.models import CuppingModel
from cupping.persistence import Cupping

from factories import SessionFactory


@pytest.fixture()
def session_and_cupping(cupping_model):
    session = SessionFactory()
    cupping_model.session_id = session.id
    return (session, cupping_model)


def test_cupping_create(session_and_cupping):
    session, cupping_model = session_and_cupping
    cupping_model.descriptors = ['berry', 'fruit']
    cupping_model.defects = ['sour', '123']
    cupping_model.notes = 'pretty good'
    cupping_model.is_sample = True

    cupping = Cupping.from_model(cupping_model)
    commit_session(_raise=True)

    assert cupping.id
    assert cupping.session_id == session.id
    assert cupping.scores == cupping_model.scores
    assert cupping.overall_score == cupping_model.overall_score
    assert cupping.descriptors == ['berry', 'fruit']
    assert cupping.defects == ['sour', '123']
    assert cupping.notes == 'pretty good'
    assert cupping.is_sample == True

    # Test the forward relationship
    assert cupping.session.id == session.id


def test_cupping_create_default_values(session_and_cupping):
    session, cupping_model = session_and_cupping
    cupping = Cupping.from_model(cupping_model)
    commit_session(_raise=True)

    assert cupping.defects == None
    assert cupping.descriptors == None
    assert cupping.is_sample == False


def test_cupping_create_scores_requires_dict(session_and_cupping):
    session, cupping_model = session_and_cupping
    cupping_model.scores = [{'Aroma': 8, 'Flavor': 6.5}]
    with pytest.raises(ValueError) as e:
        Cupping.from_model(cupping_model)

    assert 'Scores must be a mapping of name to numeric value' in str(e)


def test_cupping_create_scores_falsey(session_and_cupping):
    session, cupping_model = session_and_cupping
    cupping_model.scores = []

    cupping = Cupping.from_model(cupping_model)
    commit_session(_raise=True)
    assert cupping.scores == None


# def test_cupping_create_descriptors_requires_list(session):
#     scores = {'Aroma': 8, 'Flavor': 6.5}
#     data = {
#             'scores': scores,
#             'overallScore': 88.5,
#             'descriptors': 'yummy',
#     }
#     with pytest.raises(ValueError) as e:
#         Cupping.create(data, session=session)
#
#     assert 'descriptors must be a list of strings' in str(e)
#
#
# def test_cupping_create_defects_requires_list(session):
#     scores = {'Aroma': 8, 'Flavor': 6.5}
#     data = {
#             'scores': scores,
#             'overallScore': 88.5,
#             'defects': 'yummy',
#     }
#     with pytest.raises(ValueError) as e:
#         Cupping.create(data, session=session)
#
#     assert 'defects must be a list of strings' in str(e)
#
#
