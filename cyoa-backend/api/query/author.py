import graphene

from story.models import Author


class AuthorType(graphene.ObjectType):

    class Meta:
        interfaces = (graphene.Node, )
    
    first_name = graphene.String()
    last_name = graphene.String()
    twitter_account = graphene.String()

    stories_connection = graphene.ConnectionField('api.query.story.StoryConnection')

    def resolve_stories_connection(self, info, **kwargs):
        return info.context.loaders.stories_from_author.load(self.id)

    @classmethod
    def is_type_of(cls, root, info):
        return isinstance(root, Author)

    @classmethod
    def get_node(cls, info, id):
        return info.context.loaders.author.load(int(id))


class Query(graphene.ObjectType):
    pass
