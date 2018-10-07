import graphene

from .character import Query as CharacterQuery
from .choice import Query as ChoiceQuery
from .passage import Query as PassageQuery
from .story import Query as StoryQuery

class Query(
    CharacterQuery,
    ChoiceQuery,
    PassageQuery,
    StoryQuery,
):
    node = graphene.Node.Field()