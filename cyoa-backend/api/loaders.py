from collections import defaultdict

from promise import Promise
from promise.dataloader import DataLoader
from django.utils.functional import cached_property

from story.models import Passage, Choice, Character, Story


class StoryLoader(DataLoader):
    def batch_load_fn(self, story_ids):
        return Promise.resolve(self.get_stories(story_ids))

    def get_stories(self, story_ids):
        stories = Story.objects.filter(id__in=story_ids)
        story_map = {}
        for story in stories:
            story_map[story.id] = story
        return [story_map[story_id] for story_id in story_ids]


class PassageLoader(DataLoader):
    def batch_load_fn(self, passage_ids):
        return Promise.resolve(self.get_passages(passage_ids))

    def get_passages(self, passage_ids):
        passages = Passage.objects.filter(id__in=passage_ids)
        passage_map = {}
        for passage in passages:
            passage_map[passage.id] = passage
        return [passage_map[passage_id] for passage_id in passage_ids]


class PassageFromStoryLoader(DataLoader):
    def batch_load_fn(self, story_ids):
        return Promise.resolve(self.get_passages(story_ids))

    def get_passages(self, story_ids):
        passages = Passage.objects.filter(story_id__in=story_ids)
        passage_map = defaultdict(list)
        for passage in passages:
            passage_map[passage.story_id].append(passage)
        return [passage_map[story_id] for story_id in story_ids]


class PassageFromPovCharacterLoader(DataLoader):
    def batch_load_fn(self, pov_character_ids):
        return Promise.resolve(self.get_passages(pov_character_ids))

    def get_passages(self, pov_character_ids):
        passages = Passage.objects.filter(pov_character_id__in=pov_character_ids)
        passage_map = defaultdict(list)
        for passage in passages:
            passage_map[passage.pov_character_id].append(passage)
        return [passage_map[pov_character_id] for pov_character_id in pov_character_ids]


class ChoiceLoader(DataLoader):
    def batch_load_fn(self, choice_ids):
        return Promise.resolve(self.get_choices(choice_ids))

    def get_choices(self, choice_ids):
        choices = Choice.objects.filter(id__in=choice_ids)
        choice_map = {}
        for choice in choices:
            choice_map[choice.id] = choice
        return [choice_map[choice_id] for choice_id in choice_ids]


class ChoiceFromToPassageLoader(DataLoader):
    def batch_load_fn(self, to_passage_ids):
        return Promise.resolve(self.get_choices(to_passage_ids))

    def get_choices(self, to_passage_ids):
        choices = Choice.objects.filter(to_passage_id__in=to_passage_ids)
        choice_map = defaultdict(list)
        for choice in choices:
            choice_map[choice.to_passage_id].append(choice)
        return [choice_map[to_passage_id] for to_passage_id in to_passage_ids]


class ChoiceFromFromPassageLoader(DataLoader):
    def batch_load_fn(self, from_passage_ids):
        return Promise.resolve(self.get_choices(from_passage_ids))

    def get_choices(self, from_passage_ids):
        choices = Choice.objects.filter(from_passage_id__in=from_passage_ids)
        choice_map = defaultdict(list)
        for choice in choices:
            choice_map[choice.from_passage_id].append(choice)
        return [choice_map[from_passage_id] for from_passage_id in from_passage_ids]


class CharacterLoader(DataLoader):
    def batch_load_fn(self, character_ids):
        return Promise.resolve(self.get_characters(character_ids))

    def get_characters(self, character_ids):
        characters = Character.objects.filter(id__in=character_ids)
        character_map = {}
        for character in characters:
            character_map[character.id] = character
        return [character_map[character_id] for character_id in character_ids]


class Loaders:

    @cached_property
    def story(self):
        return StoryLoader()

    @cached_property
    def passage(self):
        return PassageLoader()

    @cached_property
    def passage_from_story(self):
        return PassageFromStoryLoader()

    @cached_property
    def passage_from_pov_character(self):
        return PassageFromPovCharacterLoader()

    @cached_property
    def choice(self):
        return ChoiceLoader()

    @cached_property
    def choice_from_frompassage(self):
        return ChoiceFromFromPassageLoader()

    @cached_property
    def choice_from_topassage(self):
        return ChoiceFromToPassageLoader()

    @cached_property
    def character(self):
        return CharacterLoader()

