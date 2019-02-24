from typing import Any, List

import graphene

from story.models import Character, Passage


class CharacterType(graphene.ObjectType):

    class Meta:
        interfaces = (graphene.Node, )

    name = graphene.String()
    in_passage_connection = graphene.ConnectionField('api.query.passage.PassageConnection')

    @staticmethod
    def resolve_in_passage_connection(root: Character, info: graphene.ResolveInfo, **_) -> List[Passage]:
        return info.context.loaders.passage_from_pov_character.load(root.id)

    @classmethod
    def is_type_of(cls, root: Any, _: graphene.ResolveInfo) -> bool:
        return isinstance(root, Character)

    @classmethod
    def get_node(cls, info: graphene.ResolveInfo, id_: str) -> Character:
        return info.context.loaders.character.load(int(id_))



class Query(graphene.ObjectType):
    pass
