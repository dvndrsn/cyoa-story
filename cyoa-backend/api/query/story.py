from typing import Any, List, Iterable

import graphene
from promise import Promise

from story.models import Story, Author, Passage


class StoryType(graphene.ObjectType):

    class Meta:
        interfaces = (graphene.Node, )

    title = graphene.String()
    subtitle = graphene.String()
    description = graphene.String()
    published_year = graphene.String()

    author = graphene.Field('api.query.author.AuthorType')
    passages = graphene.ConnectionField('api.query.passage.PassageConnection')

    @staticmethod
    def resolve_author(root: Story, info: graphene.ResolveInfo) -> Promise[Author]:
        return info.context.loaders.author.load(root.author_id)

    @staticmethod
    def resolve_passages(root: Story, info: graphene.ResolveInfo, **_) -> Promise[List[Passage]]:
        return info.context.loaders.passage_from_story.load(root.id)

    @classmethod
    def is_type_of(cls, root: Any, _: graphene.ResolveInfo) -> bool:
        return isinstance(root, Story)

    @classmethod
    def get_node(cls, info: graphene.ResolveInfo, id_: str) -> Promise[Story]:
        return info.context.loaders.story.load(int(id_))


class StoryConnection(graphene.Connection):

    class Meta:
        node = StoryType


class Query(graphene.ObjectType):
    stories = graphene.ConnectionField(StoryConnection)
    node = graphene.Node.Field()

    @staticmethod
    def resolve_stories(root, _: graphene.ResolveInfo, **__) -> Iterable[Story]:
        return Story.objects.all()
