from schematics.exceptions import ValidationError
from schematics.models import Model
from schematics.types import (
        BooleanType,
        DecimalType,
        DictType,
        IntType,
        ListType,
        StringType,
)


class ScoresType(DictType):
    def validate_nonempty(self, value):
        if not value:
            raise ValidationError('This field is required.')
        return value


class CuppingModel(Model):
    session_id = IntType()
    scores = ScoresType(DecimalType, required=True)
    overall_score = DecimalType(required=True, min_value=0, max_value=100,
            serialized_name='overallScore')
    descriptors = ListType(StringType)
    defects = ListType(StringType)
    notes = StringType()
    is_sample = BooleanType(default=False, serialized_name='isSample')
