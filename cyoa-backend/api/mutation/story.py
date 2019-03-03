from typing import Any

import graphene

from api.util import from_global_id
from story.services.story import StoryService


class CreateStory(graphene.ClientIDMutation):

    class Input:
        title = graphene.String()
        subtitle = graphene.String()
        description = graphene.String()
        published_year = graphene.String()
        author_id = graphene.ID()

    story = graphene.Field('api.query.story.StoryType')

    @classmethod
    def mutate_and_get_payload(cls, root: Any, info: graphene.ResolveInfo, **input_data: dict) -> 'CreateStory':
        serializer = StoryService(data={
            'title': input_data['title'],
            'subtitle': input_data['subtitle'],
            'description': input_data['description'],
            'published_year': input_data['published_year'],
            'author_id': from_global_id(input_data['author_id']).type_id
        })
        serializer.is_valid(raise_exception=True)
        story = serializer.save()
        return cls(story=story)


class UpdateStory(graphene.ClientIDMutation):

    class Input:
        story_id = graphene.ID()
        title = graphene.String()
        subtitle = graphene.String()
        description = graphene.String()
        published_year = graphene.String()
        author_id = graphene.ID()

    story = graphene.Field('api.query.story.StoryType')

    @classmethod
    def mutate_and_get_payload(cls, root: Any, info: graphene.ResolveInfo, **input_data: dict) -> 'UpdateStory':
        story = from_global_id(input_data['story_id'])
        serializer = StoryService.for_instance(story.type_id, data={
            'title': input_data['title'],
            'subtitle': input_data['subtitle'],
            'description': input_data['description'],
            'published_year': input_data['published_year'],
            'author_id': from_global_id(input_data['author_id']).type_id
        })
        serializer.is_valid(raise_exception=True)
        story = serializer.save()
        return cls(story=story)


class Mutation(graphene.ObjectType):
    create_story = CreateStory.Field()
    update_story = UpdateStory.Field()
