from .base import CuppingServiceBaseMixin
from .cupping import Cupping
from ..db import dbtransaction
from ..db.mixins import Base

from sqlalchemy import (
        Boolean,
        Column,
        Integer,
        Numeric,
        String,
)
from sqlalchemy.orm import relationship


class Session(CuppingServiceBaseMixin, Base):
    """A group of cuppings."""
    __tablename__ = 'sessions'

    name = Column(String(length=127))

    form_name = Column(String(length=127))

    account_id = Column(Integer, nullable=True)

    user_id = Column(Integer, nullable=True)

    cuppings = relationship('Cupping', order_by='Cupping.id', back_populates='session')

    @classmethod
    def create(cls, data):
        with dbtransaction():
            session = cls(
                    name=data['name'],
                    form_name=data['formName'],
            )
            session.save()
            session.flush()

            cuppings = [
                    Cupping.create(c, session=session) \
                    for c in data.get('cuppings', ())
            ]

            return session
