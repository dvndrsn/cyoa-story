from typing import Any, List

import graphene
from promise import Promise

from story.models import Passage, Story, Character, Choice


class PassageType(graphene.ObjectType):

    class Meta:
        interfaces = (graphene.Node, )

    name = graphene.String()
    description = graphene.String()
    is_ending = graphene.Boolean()

    story = graphene.Field('api.query.story.StoryType')
    pov_character = graphene.Field('api.query.character.CharacterType')
    all_choices = graphene.List('api.query.choice.ChoiceType')
    from_choice_connection = graphene.ConnectionField('api.query.choice.ChoiceConnection')

    @staticmethod
    def resolve_story(root: Passage, info: graphene.ResolveInfo) -> Promise[Story]:
        return info.context.loaders.story.load(root.story_id)

    @staticmethod
    def resolve_pov_character(root: Passage, info: graphene.ResolveInfo) -> Promise[Character]:
        return info.context.loaders.character.load(root.pov_character_id)

    @staticmethod
    def resolve_all_choices(root: Passage, info: graphene.ResolveInfo) -> Promise[List[Choice]]:
        return info.context.loaders.choice_from_frompassage.load(root.id)

    @staticmethod
    def resolve_from_choice_connection(root: Passage, info: graphene.ResolveInfo, **_) -> Promise[List[Choice]]:
        return info.context.loaders.choice_from_topassage.load(root.id)

    @classmethod
    def is_type_of(cls, root: Any, _: graphene.ResolveInfo) -> bool:
        return isinstance(root, Passage)

    @classmethod
    def get_node(cls, info: graphene.ResolveInfo, id_: str) -> Promise[Passage]:
        return info.context.loaders.passage.load(int(id_))


class PassageConnection(graphene.Connection):

    class Meta:
        node = PassageType


class Query(graphene.ObjectType):
    pass
