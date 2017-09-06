import os
import sys
import pytest
import random

from pathlib import Path

CWD = Path(__file__).resolve().parent
code_dir = CWD / '../serverless'
lib_dir = CWD / '../serverless/lib'

sys.path.append(str(code_dir))
sys.path.append(str(lib_dir))

os.environ.update({
    'CUPPING_DB_PASSWORD': '',
    'CUPPING_DB_HOST': 'cupping-dev-postgres',
    'CUPPING_DB_USERNAME': 'postgres',
})

from cupping.models import (
        Cupping,
        Session,
)
from cupping.db import (
        _drop_tables,
        close_db,
        get_session,
        setup_db,
)


def pytest_configure(config):
    """Called at the start of the entire test run"""
    setup_db(is_test=True)


def pytest_unconfigure(config):
    """Called at the end of a test run"""
    close_db()
    _drop_tables()


def pytest_runtest_teardown(item, nextitem):
    """Called at the end of each test"""
    get_session().rollback()


@pytest.fixture()
def session():
    return Session()


@pytest.fixture()
def valid_session():
    return Session({
        'name': 'Test Session',
        'form_name': 'SCAA',
    })


@pytest.fixture()
def cuppings():
    return [
        Cupping({
            'session_id': 10,
            'scores': {
                'Aroma': random.randint(1, 10),
                'Flavor': random.randint(1, 10),
            },
            'overall_score': 88.5,
        }) for i in range(3)
    ]
