import graphene

from story.models import Author


class AuthorType(graphene.ObjectType):

    class Meta:
        interfaces = (graphene.Node, )

    first_name = graphene.String()
    last_name = graphene.String()
    twitter_account = graphene.String()

    stories_connection = graphene.ConnectionField('api.query.story.StoryConnection')

    @staticmethod
    def resolve_stories_connection(root: Author, info: graphene.ResolveInfo, **_):
        return info.context.loaders.stories_from_author.load(root.id)

    @classmethod
    def is_type_of(cls, root: Author, _: graphene.ResolveInfo):
        return isinstance(root, Author)

    @classmethod
    def get_node(cls, info: graphene.ResolveInfo, id_: str):
        return info.context.loaders.author.load(int(id_))


class Query(graphene.ObjectType):
    pass
