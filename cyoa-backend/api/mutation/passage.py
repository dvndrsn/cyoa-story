import graphene


class CreatePassage(graphene.ClientIDMutation):
    
    class Input:
        name = graphene.String()
        description = graphene.String()
        is_ending = graphene.Boolean()
        pov_character_id = graphene.ID()
        story_id = graphene.ID()

    passage = graphene.Field('api.query.passage.PassageType')

    @classmethod
    def mutate_and_get_payload(cls, info, **input_data):
        return cls(passage=None)


class UpdatePassage(graphene.ClientIDMutation):
    
    class Input:
        passage_id = graphene.ID()
        name = graphene.String()
        description = graphene.String()
        is_ending = graphene.Boolean()
        pov_character_id = graphene.ID()
        story_id = graphene.ID()
        
    passage = graphene.Field('api.query.passage.PassageType')

    @classmethod
    def mutate_and_get_payload(cls, info, **input_data):
        return cls(passage=None)


class Mutation(graphene.ObjectType):
    create_passage = CreatePassage.Field()
    update_passage = UpdatePassage.Field()
