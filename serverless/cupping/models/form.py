import itertools

from mongoengine import Document
from mongoengine.fields import *

from common.db.models import AddedOrUpdatedEmbedded

from cupping_mixins import CuppingUserMixin


__all__ = ('CuppingForm', )


class CuppingForm(Document, CuppingUserMixin):
    """The custom definition of a cupping form."""

    account_id = IntField(db_field='_account_id', required=True)

    name = StringField(max_length=32, required=True)

    added_by = EmbeddedDocumentField(AddedOrUpdatedEmbedded, required=True)

    columns = ListField(StringField())

    meta = {
            'collection': 'cupping_forms',
            'indexes': ['added_by.uid'],
    }

    def __unicode__(self):
        return self.name

    @staticmethod
    def for_user(user):
        """Return a queryset to fetch all CuppingForms for a user."""
        return CuppingForm.objects(added_by__uid=user.id)

    @staticmethod
    def for_account(account):
        """Return a queryset to fetch all CuppingForms for an account."""
        return CuppingForm.objects(account_id=account.id)

    @staticmethod
    def form_choices_for_user(user):
        """Return a form choice list for all cupping forms for a user.

        This is used to display a list of possible cupping forms when a user
        goes to cup coffee.

        """
        return [(c.id, unicode(c)) for c in CuppingForm.for_user(user)]

    @staticmethod
    def get_cupping_fields_for_user(user):
        """Return a sortd list of all the possible columns a user could have
        used to cup coffee.

        """
        fields = set()
        for f in CuppingForm.for_user(user):
            fields.update(set(f.columns))
        return sorted(list(fields))

    @staticmethod
    def get_cupping_fields_for_account(account):
        """Return a sorted list of all the possible columns an account could have
        used to cup coffee.

        """
        return sorted(list(set(itertools.chain.from_iterable([f.columns for f in CuppingForm.for_account(account)]))))
