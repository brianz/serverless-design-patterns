import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType

from ..persistence.session import Session
from ..persistence.queries import get_sessions


class SessionObject(SQLAlchemyObjectType):
    class Meta:
        model = Session


class Query(graphene.ObjectType):
    cuppings = graphene.List(SessionObject)

    hello = graphene.String(name=graphene.String(default_value="stranger"))

    def resolve_cuppings(self, info):
        #import pdb; pdb.set_trace()
        return get_sessions()

    def resolve_hello(self, info, name):
        return 'Hello ' + name


schema = graphene.Schema(query=Query)
