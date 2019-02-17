import graphene

from .query import Query


SCHEMA = graphene.Schema(query=Query)
