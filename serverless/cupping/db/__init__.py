import contextlib

from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool


from ..constants import (
        DB_ENGINE,
        DB_HOST,
        DB_NAME,
        DB_PASSWORD,
        DB_PORT,
        DB_USERNAME,
        SQLITE,
        POSTGRESQL,
)

__session_factory = None
__session = None
__engine = None
__is_test = False



def setup_db(*, is_test=False, **db_config):
    global __engine
    global __is_test

    if __engine:
        return

    connection_string = get_connection_string()
    connection_kwargs = db_config.get('connection_kwargs', {})

    # TODO - debug stuff
    # connection_kwargs['echo'] = True
    # connection_kwargs['poolclass'] = NullPool

    session_kwargs = db_config.get('session_kwargs', {})

    if 'test_' in connection_string or connection_string == 'sqlite://' or is_test:
        __is_test = True

    print('Connecting to: %s' % (connection_string, ))
    __engine = create_engine(connection_string, **connection_kwargs)
    create_tables()
    get_session(**session_kwargs)


def get_connection_string():
    """Return a connection string for sqlalchemy::

        dialect+driver://username:password@host:port/database

    """
    if DB_ENGINE not in (SQLITE, POSTGRESQL):
        raise ValueError(
                'Invalid database engine specified: %s. Only sqlite' \
                ' and postgresql are supported' % (DB_ENGINE, ))

    if DB_ENGINE == SQLITE:
        return 'sqlite://%s' % kwargs.get('filename', '')

    return 'postgresql://%s:%s@%s:%s/%s' % (
            DB_USERNAME,
            DB_PASSWORD,
            DB_HOST,
            DB_PORT,
            DB_NAME,
    )


def close_db():
    if not __session:
        return
    try:
        __session.commit()
    except:
        __session.rollback()
    finally:
        __session.close()


def commit_session():
    try:
        __session.commit()
    except:
        __session.rollback()


def _get_metadata():
    from .base import Base
    return Base.metadata


def create_tables():
    assert __engine
    meta = _get_metadata()
    meta.create_all(__engine)

def _drop_tables(*, force=False):
    if not __is_test and not force:
        return
    assert __engine
    meta = _get_metadata()
    meta.drop_all(__engine)


def _clear_tables(*, force=False):
    if not __is_test and not force:
        return

    assert __engine

    meta = _get_metadata()
    with contextlib.closing(__engine.connect()) as con:
        trans = con.begin()
        for table in reversed(meta.sorted_tables):
            try:
                con.execute(table.delete())
            except:
                pass
        trans.commit()


def get_session(**kwargs):
    setup_db()

    assert __engine
    global __session
    global __session_factory

    if __session is not None:
        return __session

    if __session_factory is None:
        __session_factory = sessionmaker(bind=__engine, **kwargs)

    __session = __session_factory()
    return __session


@contextmanager
def dbtransaction():
    s = get_session()
    yield s
    try:
        s.commit()
    except:
        s.rollback()
        raise
