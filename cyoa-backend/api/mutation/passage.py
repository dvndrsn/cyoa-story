from typing import Any

import graphene

from api.util import from_global_id
from story.services.passage import PassageService


class CreatePassage(graphene.ClientIDMutation):

    class Input:
        name = graphene.String()
        description = graphene.String()
        is_ending = graphene.Boolean()
        character_id = graphene.ID()
        story_id = graphene.ID()

    passage = graphene.Field('api.query.passage.PassageType')

    @classmethod
    def mutate_and_get_payload(cls, root: Any, info: graphene.ResolveInfo, **input_data: dict) -> 'CreatePassage':
        serializer = PassageService(data={
            'name': input_data['name'],
            'description': input_data['description'],
            'is_ending': input_data['is_ending'],
            'story_id': from_global_id(input_data['story_id']).type_id,
            'character_id': from_global_id(input_data['character_id']).type_id,
        })
        serializer.is_valid(raise_exception=True)
        passage = serializer.save()
        return cls(passage=passage)


class UpdatePassage(graphene.ClientIDMutation):

    class Input:
        passage_id = graphene.ID()
        name = graphene.String()
        description = graphene.String()
        is_ending = graphene.Boolean()
        character_id = graphene.ID()
        story_id = graphene.ID()

    passage = graphene.Field('api.query.passage.PassageType')

    @classmethod
    def mutate_and_get_payload(cls, root: Any, info: graphene.ResolveInfo, **input_data: dict) -> 'UpdatePassage':
        decoded = from_global_id(input_data['passage_id'])
        serializer = PassageService.for_instance(decoded.type_id, data={
            'name': input_data['name'],
            'description': input_data['description'],
            'is_ending': input_data['is_ending'],
            'story_id': from_global_id(input_data['story_id']).type_id,
            'character_id': from_global_id(input_data['character_id']).type_id,
        })
        serializer.is_valid(raise_exception=True)
        passage = serializer.save()
        return cls(passage=passage)


class Mutation(graphene.ObjectType):
    create_passage = CreatePassage.Field()
    update_passage = UpdatePassage.Field()
