from .base import CuppingServiceBaseMixin
from .cupping import Cupping
from ..db import dbtransaction
from ..db.base import Base

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

    # def __unicode__(self):
    #     return "%d roasts" % (len(self.scores), )
    #
    # @property
    # def is_sample_session(self):
    #     cuppings = self.get_cuppings()
    #     if len(cuppings) < 1:
    #         return False
    #     elif cuppings[0].is_sample:
    #         return True
    #     return False
    #
    # def add_cupping(self, cupping):
    #     """Add an existing cupping into this session."""
    #     self.cuppings.append(cupping.id)
    #     if cupping.score:
    #         self.scores.append((unicode(cupping), cupping.score))
    #
    # def get_cuppings(self):
    #     """Dereference the cuppings for this session."""
    #     if not hasattr(self, '_cuppings'):
    #         self._cuppings = list(Cupping.objects(id__in=self.cuppings))
    #
    #     return self._cuppings

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
                    for c in data['cuppings']
            ]

            return session
        #'name': 'Cupping session', 'form': 'custom-form'
