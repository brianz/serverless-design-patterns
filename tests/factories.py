import factory

from factory.fuzzy import FuzzyChoice

from cupping.models import Session
from cupping.db import commit_session


class BaseFactory(factory.Factory):

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        inst = model_class(*args, **kwargs)
        inst.save()
        commit_session()
        return inst


class SessionFactory(BaseFactory):
    class Meta:
        model = Session

    name = factory.Sequence(lambda n: u'Cupping session %d' % n)
    form_name = FuzzyChoice(('SCAA', 'COE'))
