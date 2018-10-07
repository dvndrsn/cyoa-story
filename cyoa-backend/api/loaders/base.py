from .story import StoryLoaders
from .passage import PassageLoaders
from .choice import ChoiceLoaders
from .character import CharacterLoaders


class Loaders(
    StoryLoaders,
    PassageLoaders,
    ChoiceLoaders,
    CharacterLoaders,
):
    pass
