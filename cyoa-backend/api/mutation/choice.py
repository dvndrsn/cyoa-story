import graphene


class CreateChoice(graphene.ClientIDMutation):
    
    class Input:
        name = graphene.String()
        is_main_story = graphene.Boolean()
        from_passage_id = graphene.ID()
        to_passage_id = graphene.ID()

    choice = graphene.Field('api.query.choice.ChoiceType')

    @classmethod
    def mutate_and_get_payload(cls, info, **input_data):
        return cls(choice=None)


class UpdateChoice(graphene.ClientIDMutation):
    
    class Input:
        choice_id = graphene.ID()
        name = graphene.String()
        is_main_story = graphene.Boolean()
        from_passage_id = graphene.ID()
        to_passage_id = graphene.ID()
        
    choice = graphene.Field('api.query.choice.ChoiceType')

    @classmethod
    def mutate_and_get_payload(cls, info, **input_data):
        return cls(choice=None)


class Mutation(graphene.ObjectType):
    create_choice = CreateChoice.Field()
    update_choice = UpdateChoice.Field()
