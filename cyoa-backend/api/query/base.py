import graphene

from .character import Query as CharacterQuery
from .choice import Query as ChoiceQuery
from .passage import Query as PassageQuery
from .story import Query as StoryQuery
from .author import Query as AuthorQuery


class Query(
        CharacterQuery,
        ChoiceQuery,
        PassageQuery,
        StoryQuery,
        AuthorQuery,
):
    node = graphene.Node.Field()
