import graphene
from cursor_pagination import CursorPaginator
import graphene_django

from story.models import Passage, Story, Character, Choice


class CharacterType(graphene.ObjectType):

    class Meta:
        interfaces = (graphene.Node, )
    
    name = graphene.String()

    @classmethod
    def get_node(cls, info, id):
        return Character.objects.get(pk=id)


class ChoiceType(graphene.ObjectType):

    class Meta:
        interfaces = (graphene.Node, )

    description = graphene.String()
    is_main_story = graphene.Boolean()

    to_passage = graphene.Field('api.schema.PassageType') 


class ChoiceEdge(graphene.ObjectType):
    cursor = graphene.String()
    node = graphene.Field('api.schema.ChoiceType')


class ChoiceConnection(graphene.ObjectType):
    choices = graphene.List(ChoiceType)
    total_choices = graphene.Int()

    edges = graphene.List(ChoiceEdge)
    page_info = graphene.Field(graphene.PageInfo)

    def resolve_choices(self, info):
        return self.paginator.queryset.all()

    def resolve_total_choices(self, info):
        return self.paginator.queryset.count()

    def resolve_edges(self, info):
        return [ChoiceEdge(node=edge, cursor=self.paginator.cursor(edge)) for edge in self]

    def resolve_page_info(self, info):
        return graphene.PageInfo(
            start_cursor=self.paginator.cursor(self[0]),
            end_cursor=self.paginator.cursor(self[-1]), # "Negative indexing is not supported."
            has_previous_page=self.has_previous,
            has_next_page=self.has_next,
        )


class PassageType(graphene.ObjectType):

    class Meta:
        interfaces = (graphene.Node, )
    
    name = graphene.String()
    description = graphene.String()
    is_ending = graphene.Boolean()

    pov_character = graphene.Field(CharacterType)
    all_choices = graphene.List(ChoiceType)
    choice_connection = graphene.Field(
        'api.schema.ChoiceConnection',
        first=graphene.Int(),
        after=graphene.String(),
        last=graphene.Int(),
        before=graphene.String(),
    )

    def resolve_all_choices(self, info):
        return self.to_choices.all()

    def resolve_choice_connection(self, info, first=None, after=None, last=None, before=None):
        choices = self.to_choices.all()
        paginator = CursorPaginator(choices, ordering=('id',))
        return paginator.page(
            first=first,
            after=after,
            last=last,
            before=before,
        )

    @classmethod
    def get_node(cls, info, id):
        return Passage.objects.get(pk=id)


class PassageEdge(graphene.ObjectType):
    node = graphene.Field(PassageType)
    cursor = graphene.String()


class PassageConnection(graphene.ObjectType):
    passages = graphene.List(PassageType)
    total_passages = graphene.Int()

    edges = graphene.List(PassageEdge)
    page_info = graphene.Field(graphene.PageInfo)

    def resolve_passages(self, info):
        return self.paginator.queryset.all()

    def resolve_total_passages(self, info):
        return self.paginator.queryset.count()

    def resolve_edges(self, info):
        return [PassageEdge(node=edge, cursor=self.paginator.cursor(edge)) for edge in self]

    def resolve_page_info(self, info):
        return graphene.PageInfo(
            start_cursor=self.paginator.cursor(self[0]),
            end_cursor=self.paginator.cursor(self[-1]),
            has_previous_page=self.has_previous,
            has_next_page=self.has_next,
        )


class StoryType(graphene.ObjectType):

    class Meta:
        interfaces = (graphene.Node, )

    title = graphene.String()
    subtitle = graphene.String()
    description = graphene.String()
    published_year = graphene.String()
    author = graphene.String()

    passage = graphene.Node.Field(PassageType)
    passage_connection = graphene.Field(
        PassageConnection,
        first=graphene.Int(),
        after=graphene.String(),
        last=graphene.Int(),
        before=graphene.String(),
    )

    def resolve_passage_connection(self, info, first=None, after=None, last=None, before=None):
        passages = self.passages.all()
        paginator = CursorPaginator(passages, ordering=('id',))
        return paginator.page(
            first=first,
            after=after,
            last=last,
            before=before
        )
    
    @classmethod
    def get_node(cls, info, id):
        return Story.objects.get(pk=id)
    

class StoryEdge(graphene.ObjectType):
    node = graphene.Field(StoryType)
    cursor = graphene.String()


class StoryConnection(graphene.ObjectType):
    stoies = graphene.List(StoryEdge)
    total_stories = graphene.Int()

    edges = graphene.List(PassageEdge)
    page_info = graphene.Field(graphene.PageInfo)

    def resolve_stories(self, info):
        return self.paginator.queryset.all()

    def resolve_total_stories(self, info):
        return self.paginator.queryset.count()

    def resolve_edges(self, info):
        return [StoryEdge(node=edge, cursor=self.paginator.cursor(edge)) for edge in self]

    def resolve_page_info(self, info):
        return graphene.PageInfo(
            start_cursor=self.paginator.cursor(self[0]),
            end_cursor=self.paginator.cursor(self[-1]),
            has_previous_page=self.has_previous,
            has_next_page=self.has_next,
        )


class Query(graphene.ObjectType):
    story = graphene.Node.Field(StoryType)
    story_connection = graphene.Field(
        StoryConnection,
        first=graphene.Int(),
        after=graphene.String(),
        last=graphene.Int(),
        before=graphene.String(),
    )

    def resolve_story(self, info, id):
        return Story.objects.get(id=id)

    def resolve_story_connection(self, info, first=None, after=None, last=None, before=None):
        stories = Story.objects.all()
        paginator = CursorPaginator(stories, ordering=('id',))
        return paginator.page(
            first=first,
            after=after,
            last=last,
            before=before
        )

    
schema = graphene.Schema(query=Query)
