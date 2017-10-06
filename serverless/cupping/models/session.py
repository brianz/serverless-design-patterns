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
    form_name = StringType(max_length=127, required=True, serialized_name='formName')
    account_id = IntType(serialized_name='accountId')
    user_id = IntType(serialized_name='userId')

    cuppings = ListType(ModelType(CuppingModel))
