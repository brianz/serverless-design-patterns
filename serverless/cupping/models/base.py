from sqlalchemy import (
        Column,
        Integer,
)

from ..db.base import (
        Base,
        BaseCuppingServicMixin,
)


class CuppingServiceBaseMixin(BaseCuppingServicMixin):
    id =  Column(Integer, primary_key=True)
