from factory.django import DjangoModelFactory
from factory import SubFactory

from story import models

class AuthorFactory(DjangoModelFactory):
    class Meta:
        model = models.Author

    first_name = 'Friendly'
    last_name = 'Human'
    twitter_account = '@human'


class StoryFactory(DjangoModelFactory):
    class Meta:
        model = models.Story

    title = 'Chooseable fun times'
    subtitle = 'So many paths'
    description = 'A cool story.'
    published_year = '2019'
    author = SubFactory(AuthorFactory)


class CharacterFactory(DjangoModelFactory):
    class Meta:
        model = models.Character

    name = 'Protagonist'


class PassageFactory(DjangoModelFactory):
    class Meta:
        model = models.Passage

    name = 'Passage 5'
    description = 'A wise decision'
    is_ending = False
    story = SubFactory(StoryFactory)
    pov_character = SubFactory(CharacterFactory)
