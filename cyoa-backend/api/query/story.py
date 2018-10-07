import graphene

from story.models import Story


class StoryType(graphene.ObjectType):

    class Meta:
        interfaces = (graphene.Node, )

    title = graphene.String()
    subtitle = graphene.String()
    description = graphene.String()
    published_year = graphene.String()
    date_published =graphene.String()
    author = graphene.String()

    created_at = graphene.String()
    updated_at = graphene.String()

    passage_connection = graphene.ConnectionField('api.query.passage.PassageConnection')

    def resolve_passage_connection(self, info, first=None, after=None, last=None, before=None):
        return info.context.loaders.passage_from_story.load(self.id)

    @classmethod
    def is_type_of(cls, root, info):
        return isinstance(root, Story)
    
    @classmethod
    def get_node(cls, info, id):
        return info.context.loaders.story.load(int(id))


class StoryConnection(graphene.Connection):

    class Meta:
        node = StoryType


class Query(graphene.ObjectType):
    story_connection = graphene.ConnectionField(StoryConnection)

    def resolve_story_connection(self, info, **kwargs):
        return Story.objects.all()
