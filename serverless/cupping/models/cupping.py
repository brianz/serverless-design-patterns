from .base import CuppingServiceBaseMixin
from ..db.mixins import Base

from sqlalchemy import (
        Boolean,
        Column,
        ForeignKey,
        Integer,
        Numeric,
        String,
)
from sqlalchemy.orm import relationship, validates
from sqlalchemy.dialects.postgresql import JSONB


class Cupping(CuppingServiceBaseMixin, Base):
    """An individual cupping for one object (roast)."""
    __tablename__ = 'cuppings'

    #: the `Session` this cupping is a part of
    session_id = Column(Integer, ForeignKey('sessions.id'), nullable=False)

    # `Cupping.session` refers to a `Session` instance, and on the other side, `Session.cuppings`
    # refers to a list of `Cupping` instances.
    session = relationship('Session', back_populates='cuppings')

    #: This is the real juicy bit.  `scores` is a list of key/value, where key is column name
    #: with a matching numeric score.  Note, we index on the keys to supporty querying.
    scores = Column(JSONB, nullable=False)

    #: Final score for this coffee
    total_score = Column(Numeric(decimal_return_scale=1))

    #: A list of descriptors
    descriptors = Column(JSONB, nullable=True)

    #: A list of defects
    defects = Column(JSONB, nullable=True)

    #: General notes
    notes = Column(String(length=255))

    #: tells whether or not the object is a sample
    is_sample = Column(Boolean, default=False)

    @classmethod
    def create(cls, data, session=None):
        assert session
        cupping = Cupping(
                session_id=session.id,
                scores=data['scores'],
                total_score=data['overallScore'],
                descriptors=data.get('descriptors', []),
                defects=data.get('defects', []),
                notes=data.get('notes', ''),
                is_sample=data.get('isSample', False),
        )
        cupping.save()
        return cupping
