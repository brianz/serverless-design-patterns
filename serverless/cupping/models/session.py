from cupping import Cupping
from .mixins import (
        CuppingUserMixin,
)

from schematics.models import Model
from schematics.types import StringType, DecimalType, DateTimeType


class CuppingSession(CuppingUserMixin):
    """A group of cuppings."""

    account_id = IntField(db_field='_account_id', required=True)

    added_by = EmbeddedDocumentField(AddedOrUpdatedEmbedded, required=True)

    cupping_form_id = ObjectIdField()

    scores = ListField()

    cuppings = ListField(ObjectIdField())

    meta = {
            'collection': 'cupping_sessions',
            'indexes': [
                    'added_by.uid',
                    'account_id',
            ],
    }

    def __unicode__(self):
        return "%d roasts" % (len(self.scores), )

    @permalink
    def get_absolute_url(self):
        return ('cupping-view-session', [str(self.id)])

    @property
    def is_sample_session(self):
        cuppings = self.get_cuppings()
        if len(cuppings) < 1:
            return False
        elif cuppings[0].is_sample:
            return True
        return False

    def add_cupping(self, cupping):
        """Add an existing cupping into this session."""
        self.cuppings.append(cupping.id)
        if cupping.score:
            self.scores.append((unicode(cupping), cupping.score))

    def get_cuppings(self):
        """Dereference the cuppings for this session."""
        if not hasattr(self, '_cuppings'):
            self._cuppings = list(Cupping.objects(id__in=self.cuppings))

        return self._cuppings
