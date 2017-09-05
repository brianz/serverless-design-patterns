import pytest

#from unittest.mock import MagicMock

from cupping.helpers import (
        utcnow,
)


def test_utcnow():
    assert utcnow()
