from schematics.models import Model
from schematics.types import (
        BooleanType,
        DecimalType,
        DictType,
        IntType,
        ListType,
        StringType,
)


class CuppingModel(Model):
    session_id = IntType()
    scores = DictType(DecimalType, required=True)
    overall_score = DecimalType(required=True, min_value=0, max_value=100)
    descriptors = ListType(StringType)
    defects = ListType(StringType)
    notes = StringType()
    is_sample = BooleanType(default=False)
