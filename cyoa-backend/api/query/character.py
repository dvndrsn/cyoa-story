import graphene

from story.models import Character


class CharacterType(graphene.ObjectType):

    class Meta:
        interfaces = (graphene.Node, )
    
    name = graphene.String()
    in_passage_connection = graphene.ConnectionField('api.query.passage.PassageConnection')

    def resolve_in_passage_connection(self, info, **kwargs):
        return info.context.loaders.passage_from_pov_character.load(self.id)

    @classmethod
    def is_type_of(cls, root, info):
        return isinstance(root, Character)

    @classmethod
    def get_node(cls, info, id):
        return info.context.loaders.character.load(int(id))


class Query(graphene.ObjectType):
    pass