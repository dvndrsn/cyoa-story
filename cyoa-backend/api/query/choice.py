from typing import Any

import graphene
from promise import Promise

from story.models import Choice, Passage


class ChoiceType(graphene.ObjectType):

    class Meta:
        interfaces = (graphene.Node, )

    description = graphene.String()
    is_main_story = graphene.Boolean()

    from_passage = graphene.Field('api.query.passage.PassageType')
    to_passage = graphene.Field('api.query.passage.PassageType')

    @staticmethod
    def resolve_from_passage(root: Choice, info: graphene.ResolveInfo, **_) -> Promise[Passage]:
        return info.context.loaders.passage.load(root.from_passage_id)

    @staticmethod
    def resolve_to_passage(root: Choice, info: graphene.ResolveInfo, **_) -> Promise[Passage]:
        return info.context.loaders.passage.load(root.to_passage_id)

    @classmethod
    def is_type_of(cls, root: Any, _: graphene.ResolveInfo) -> bool:
        return isinstance(root, Choice)

    @classmethod
    def get_node(cls, info: graphene.ResolveInfo, id_: str) -> Promise[Choice]:
        return info.context.loaders.choice.load(int(id_))


class ChoiceConnection(graphene.Connection):

    class Meta:
        node = ChoiceType


class Query(graphene.ObjectType):
    pass
