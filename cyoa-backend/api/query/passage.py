import graphene

from story.models import Passage


class PassageType(graphene.ObjectType):

    class Meta:
        interfaces = (graphene.Node, )
    
    name = graphene.String()
    description = graphene.String()
    is_ending = graphene.Boolean()

    pov_character = graphene.Field('api.query.character.CharacterType')
    all_choices = graphene.List('api.query.choice.ChoiceType')
    from_choice_connection = graphene.ConnectionField('api.query.choice.ChoiceConnection')

    def resolve_pov_character(self, info):
        return info.context.loaders.character.load(self.pov_character_id)

    def resolve_all_choices(self, info):
        return info.context.loaders.choice_from_frompassage.load(self.id)

    def resolve_from_choice_connection(self, info, **kwargs):
        return info.context.loaders.choice_from_topassage.load(self.id)

    @classmethod
    def is_type_of(cls, root, info):
        return isinstance(root, Passage)

    @classmethod
    def get_node(cls, info, id):
        return info.context.loaders.passage.load(int(id))


class PassageConnection(graphene.Connection):

    class Meta:
        node = PassageType


class Query(graphene.ObjectType):
    pass
