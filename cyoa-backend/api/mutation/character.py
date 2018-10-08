import graphene


class CreateCharacter(graphene.ClientIDMutation):
    
    class Input:
        name = graphene.String()

    character = graphene.Field('api.query.character.CharacterType')

    @classmethod
    def mutate_and_get_payload(cls, info, **input_data):
        return cls(character=None)


class UpdateCharacter(graphene.ClientIDMutation):
    
    class Input:
        character_id = graphene.ID()
        name = graphene.String()
        
    character = graphene.Field('api.query.character.CharacterType')

    @classmethod
    def mutate_and_get_payload(cls, info, **input_data):
        return cls(character=None)


class Mutation(graphene.ObjectType):
    create_character = CreateCharacter.Field()
    update_character = UpdateCharacter.Field()
