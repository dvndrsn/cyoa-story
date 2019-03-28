from typing import Any, List

import graphene
from promise import Promise

from story.models import Author, Story


class AuthorDisplayNameEnum(graphene.Enum):
    FIRST_LAST = Author.DISPLAY_FIRST_LAST
    LAST_FIRST = Author.DISPLAY_LAST_FIRST


class AuthorType(graphene.ObjectType):

    class Meta:
        interfaces = (graphene.Node, )

    first_name = graphene.String()
    last_name = graphene.String()
    twitter_account = graphene.String()
    full_name = graphene.String(
        args={
            'display': graphene.Argument(
                AuthorDisplayNameEnum,
                required=True,
                description='Display format to use for Full Name of Author - default FIRST_LAST.'
            )
        }
    )

    stories = graphene.ConnectionField('api.query.story.StoryConnection')

    @staticmethod
    def resolve_stories(root: Author, info: graphene.ResolveInfo, **_) -> Promise[List[Story]]:
        return info.context.loaders.stories_from_author.load(root.id)

    @classmethod
    def is_type_of(cls, root: Any, _: graphene.ResolveInfo) -> bool:
        return isinstance(root, Author)

    @classmethod
    def get_node(cls, info: graphene.ResolveInfo, id_: str) -> Promise[Author]:
        return info.context.loaders.author.load(int(id_))

    @staticmethod
    def resolve_full_name(root: Author, info: graphene.ResolveInfo, display):
        return root.full_name(display)


class Query(graphene.ObjectType):
    node = graphene.Node.Field()
