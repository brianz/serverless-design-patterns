from accounts.cache import get_account_by_user
from common.db.models import AddedOrUpdatedEmbedded
from mongoenginepagination import Document as PaginatedDocumentMixin


class CuppingUserMixin(object):
    """Mixin which provides user convienience methods."""

    @classmethod
    def init_from_user(cls, user):
        added_by = AddedOrUpdatedEmbedded.from_user(user)
        account = get_account_by_user(user)
        return cls(added_by=added_by, account_id=account.id)
