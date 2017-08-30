from .base import CuppingServiceBaseMixin
from ..db.base import Base

from sqlalchemy import (
        Boolean,
        Column,
        Integer,
        Numeric,
        String,
)

# class ScoreEmbed:
#
#     name = StringField()
#     value = FloatField()
#
#     def __unicode__(self):
#         return u'%s - %0.1f' % (self.name, self.value)


class Cupping(CuppingServiceBaseMixin, Base):
    """An individual cupping for one object (roast)."""

    account_id = Column(Integer)
    user_id = Column(Integer)

    #: Final score for this coffee
    score = Column(Numeric(decimal_return_scale=1))

    #origin_ids = ListField(IntField(db_field='_origin_id'))

    #: the CuppingSessions this cupping is a part of
    #session_id = ObjectIdField()

    #: This is the real juicy bit.  Score are a simple key/value of column name
    #: to numeric score.  The keys are used to query.
    #scores = ListField(EmbeddedDocumentField(ScoreEmbedded))

    #: Embed the list of columns from the cupping form.  This is so that we can
    #: maintain order when displaying the results.
    #columns = ListField()

    #: A copy of the scores, but the keys are unaltered from the cupping form
    #: so that the scores can be displayed directly to the user.
    #display_scores = DictField()

    #: A list of descriptors
    #tags = ListField(StringField())

    #: A list of defects
    #defects = ListField(StringField())

    #: General notes
    notes = Column(String(length=255))

    #: Primary key back to the roast or sample
    # roast_id = IntField()

    #: The auto_inc value for the roast.
    # roast_number = IntField()

    #: The name of the roastable for this roast.
    # roastable_name = StringField()

    #: The roastable id.
    # roastable_id = IntField()

    #: tells whether or not the object is a sample
    is_sample = Column(Boolean, default=False)

    @property
    def columns_slug(self):
        """Return a slug for the cupping form columns.

        This is a quick and easy way to compare two cuppings.  If two cuppings
        have the same ``columns_slug``, they were cupped with the same form.

        """
        #return slugify(''.join(sorted(self.columns)))

    @property
    def local_timestamp(self):
        #return self.added_by.local_timestamp
        pass

    @property
    def ordered_display_scores(self):
        pass
        # for col in self.columns:
        #     yield (col, self.display_scores.get(col))

    @property
    def country_names(self):
        pass

    @property
    def form_name(self):
        pass
        #return self.get_form_name()

    def get_form_name(self, forms=None):
        pass
        # account_forms = forms or CuppingForm.objects(account_id=self.account_id)
        #
        # for form in account_forms:
        #     if self.columns == form.columns:
        #         return form.name

    def set_scores(self, scores):
        """Helper to update both sets of scores"""
        pass
        # self.display_scores = scores
        # # Don't store a score if it's null.  Note that a 0 is still valid and
        # # should be stored.
        # self.scores = [ScoreEmbedded(name=slugify(k), value=v) \
        #                for (k, v) in scores.iteritems() if v not in (None, '')]
