from schematics.models import Model
from schematics.types import (
        IntType,
        ListType,
        ModelType,
        StringType,
)

from .cupping import CuppingModel


class SessionModel(Model):
    name = StringType(max_length=127, required=True)
    form_name = StringType(max_length=127, required=True)
    account_id = IntType()
    user_id = IntType()

    cuppings = ListType(ModelType(CuppingModel))
