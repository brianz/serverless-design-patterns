from schematics.models import Model
from schematics.types import (
        IntType,
        ListType,
        DictType,
        StringType,
        DecimalType,
)


class Cupping(Model):
    session_id = IntType(required=True)
    scores = DictType(DecimalType, required=True)
    overall_score = DecimalType(required=True, min_value=0, max_value=100)
    descriptors = ListType(StringType)
    defects = ListType(StringType)
    notes = StringType()



# class Cupping(CuppingServiceBaseMixin, Base):
#     """An individual cupping for one object (roast)."""
#     __tablename__ = 'cuppings'
#
#     #: the `Session` this cupping is a part of
#     session_id = Column(Integer, ForeignKey('sessions.id'), nullable=False)
#
#     # `Cupping.session` refers to a `Session` instance, and on the other side, `Session.cuppings`
#     # refers to a list of `Cupping` instances.
#     session = relationship('Session', back_populates='cuppings')
#
#     #: This is the real juicy bit.  `scores` is a list of key/value, where key is column name
#     #: with a matching numeric score.  Note, we index on the keys to supporty querying.
#     scores = Column(JSONB, nullable=False)
#
#     #: Final score for this coffee
#     overall_score = Column(Numeric(decimal_return_scale=1))
#
#     #: A list of descriptors
#     descriptors = Column(JSONB, nullable=True)
#
#     #: A list of defects
#     defects = Column(JSONB, nullable=True)
#
#     #: General notes
#     notes = Column(String(length=255))
#
#     #: tells whether or not the object is a sample
#     is_sample = Column(Boolean, default=False)
#
#     def _validate_list_or_tuple(self, key, value):
#         if not isinstance(value, (list, tuple)):
#             raise ValueError('%s must be a list of strings' % (key, ))
#         return [str(v).strip() for v in value]
#
#     @validates('scores')
#     def validate_scores(self, key, value):
#         if not isinstance(value, dict):
#             raise ValueError('Scores must be a mapping of name to numeric value')
#         return value
#
#     @validates('descriptors')
#     def validate_descriptors(self, key, value):
#         return self._validate_list_or_tuple(key, value)
#
#     @validates('defects')
#     def validate_defects(self, key, value):
#         return self._validate_list_or_tuple(key, value)
#
#     @classmethod
#     def create(cls, data, session=None):
#         assert session
#         cupping = Cupping(
#                 session_id=session.id,
#                 scores=data['scores'],
#                 overall_score=data['overallScore'],
#                 descriptors=data.get('descriptors', []),
#                 defects=data.get('defects', []),
#                 notes=data.get('notes', ''),
#                 is_sample=data.get('isSample', False),
#         )
#         cupping.save()
#         return cupping
