from .author import Mutation as AuthorMutation
from .story import Mutation as StoryMutation
from .passage import Mutation as PassageMutation
from .character import Mutation as CharacterMutation
from .choice import Mutation as ChoiceMutation


class Mutation(
    AuthorMutation,
    StoryMutation,
    CharacterMutation,
    PassageMutation,
    ChoiceMutation,
):
    pass
