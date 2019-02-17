import graphene

from story.models import Story


class StoryType(graphene.ObjectType):

    class Meta:
        interfaces = (graphene.Node, )

    title = graphene.String()
    subtitle = graphene.String()
    description = graphene.String()
    published_year = graphene.String()

    author = graphene.Field('api.query.author.AuthorType')
    passage_connection = graphene.ConnectionField('api.query.passage.PassageConnection')

    @staticmethod
    def resolve_author(root, info):
        return info.context.loaders.author.load(root.author_id)

    @staticmethod
    def resolve_passage_connection(root, info, **_):
        return info.context.loaders.passage_from_story.load(root.id)

    @classmethod
    def is_type_of(cls, root, _):
        return isinstance(root, Story)

    @classmethod
    def get_node(cls, info, id_):
        return info.context.loaders.story.load(int(id_))


class StoryConnection(graphene.Connection):

    class Meta:
        node = StoryType


class Query(graphene.ObjectType):
    story_connection = graphene.ConnectionField(StoryConnection)

    @staticmethod
    def resolve_story_connection(root, info: graphene.ResolveInfo, **_):  # pylint: disable=unused-argument
        return Story.objects.all()
