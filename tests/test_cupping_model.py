from cupping.db import dbtransaction, commit_session, get_session
from cupping.models import Cupping


def test_cupping_session_id_required():
    c = Cupping(
            session_id=123,
            scores={'aroma': 12},
            total_score=88,
    )
    c.save()
    #get_session().commit()
    #assert(c.id)


def test_session_create():
    pass
