from typing import Any, List

import graphene

from story.models import Author, Story


class AuthorType(graphene.ObjectType):

    class Meta:
        interfaces = (graphene.Node, )

    first_name = graphene.String()
    last_name = graphene.String()
    twitter_account = graphene.String()

    stories_connection = graphene.ConnectionField('api.query.story.StoryConnection')

    @staticmethod
    def resolve_stories_connection(root: Author, info: graphene.ResolveInfo, **_) -> List[Story]:
        return info.context.loaders.stories_from_author.load(root.id)

    @classmethod
    def is_type_of(cls, root: Any, _:graphene.ResolveInfo) -> bool:
        return isinstance(root, Author)

    @classmethod
    def get_node(cls, info: graphene.ResolveInfo, id_: str) -> Author:
        return info.context.loaders.author.load(int(id_))


class Query(graphene.ObjectType):
    pass
