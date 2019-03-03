from typing import Any

import graphene

from api.util import from_global_id
from story.services.character import CharacterService


class CreateCharacter(graphene.ClientIDMutation):

    class Input:
        name = graphene.String()

    character = graphene.Field('api.query.character.CharacterType')

    @classmethod
    def mutate_and_get_payload(cls, root: Any, info: graphene.ResolveInfo, **input_data: dict) -> 'CreateCharacter':
        serializer = CharacterService(data={
            'name': input_data['name']
        })
        serializer.is_valid(raise_exception=True)
        character = serializer.save()
        return cls(character=character)


class UpdateCharacter(graphene.ClientIDMutation):

    class Input:
        character_id = graphene.ID()
        name = graphene.String()

    character = graphene.Field('api.query.character.CharacterType')

    @classmethod
    def mutate_and_get_payload(cls, root: Any, info: graphene.ResolveInfo, **input_data: dict) -> 'UpdateCharacter':
        decoded = from_global_id(input_data['character_id'])
        serializer = CharacterService.for_instance(decoded.type_id, data={
            'name': input_data['name']
        })
        serializer.is_valid(raise_exception=True)
        character = serializer.save()
        return cls(character=character)


class Mutation(graphene.ObjectType):
    create_character = CreateCharacter.Field()
    update_character = UpdateCharacter.Field()
