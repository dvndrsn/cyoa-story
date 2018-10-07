import graphene

from story.models import Choice


class ChoiceType(graphene.ObjectType):

    class Meta:
        interfaces = (graphene.Node, )

    description = graphene.String()
    is_main_story = graphene.Boolean()

    from_passage = graphene.Field('api.query.passage.PassageType')
    to_passage = graphene.Field('api.query.passage.PassageType')

    @classmethod
    def is_type_of(cls, root, info):
        return isinstance(root, Choice)

    @classmethod
    def get_node(cls, info, id):
        return info.context.loaders.choice.load(int(id))


class ChoiceConnection(graphene.Connection):

    class Meta:
        node = ChoiceType


class Query(graphene.ObjectType):
    pass