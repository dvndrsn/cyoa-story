import graphene
import graphene_django

from story.models import Passage, Story, Character, Choice


class CharacterType(graphene.ObjectType):

    class Meta:
        interfaces = (graphene.Node, )
    
    name = graphene.String()
    in_passage_connection = graphene.ConnectionField('api.schema.PassageConnection')

    def resolve_in_passage_connection(self, info, **kwargs):
        return info.context.loaders.passage_from_pov_character.load(self.id)

    @classmethod
    def is_type_of(cls, root, info):
        return isinstance(root, Character)

    @classmethod
    def get_node(cls, info, id):
        return info.context.loaders.character.load(int(id))


class ChoiceType(graphene.ObjectType):

    class Meta:
        interfaces = (graphene.Node, )

    description = graphene.String()
    is_main_story = graphene.Boolean()

    from_passage = graphene.Field('api.schema.PassageType')
    to_passage = graphene.Field('api.schema.PassageType')

    @classmethod
    def is_type_of(cls, root, info):
        return isinstance(root, Choice)

    @classmethod
    def get_node(cls, info, id):
        return info.context.loaders.choice.load(int(id))


class ChoiceConnection(graphene.Connection):

    class Meta:
        node = ChoiceType


class PassageType(graphene.ObjectType):

    class Meta:
        interfaces = (graphene.Node, )
    
    name = graphene.String()
    description = graphene.String()
    is_ending = graphene.Boolean()

    pov_character = graphene.Field(CharacterType)
    all_choices = graphene.List(ChoiceType)
    from_choice_connection = graphene.ConnectionField(ChoiceConnection)

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

    passage_connection = graphene.ConnectionField(PassageConnection)

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
    node = graphene.Node.Field()

    def resolve_story_connection(self, info, first=None, after=None, last=None, before=None):
        return Story.objects.all()


schema = graphene.Schema(query=Query)
