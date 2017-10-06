from ..db import dbtransaction, session_getter

from .session import Session


@session_getter
def get_session_by_id(session, _id, **kwargs):
    #if 'active' not in kwargs:
    #kwargs['active'] = True
    kwargs['id'] = _id
    return session.query(Session).filter_by(**kwargs).first()
