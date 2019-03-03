import graphene

from api.util import from_global_id
from story.services.choice import ChoiceService


class CreateChoice(graphene.ClientIDMutation):

    class Input:
        description = graphene.String()
        is_main_story = graphene.Boolean()
        from_passage_id = graphene.ID()
        to_passage_id = graphene.ID()

    choice = graphene.Field('api.query.choice.ChoiceType')

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input_data):
        serializer = ChoiceService(data={
            'description': input_data['description'],
            'is_main_story': input_data['is_main_story'],
            'from_passage_id': from_global_id(input_data['from_passage_id']).type_id,
            'to_passage_id': from_global_id(input_data['to_passage_id']).type_id,
        })
        serializer.is_valid(raise_exception=True)
        choice = serializer.save()
        return cls(choice=choice)


class UpdateChoice(graphene.ClientIDMutation):

    class Input:
        choice_id = graphene.ID()
        description = graphene.String()
        is_main_story = graphene.Boolean()
        from_passage_id = graphene.ID()
        to_passage_id = graphene.ID()

    choice = graphene.Field('api.query.choice.ChoiceType')

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input_data):
        decoded = from_global_id(input_data['choice_id'])
        serializer = ChoiceService.for_instance(decoded.type_id, data={
            'description': input_data['description'],
            'is_main_story': input_data['is_main_story'],
            'from_passage_id': from_global_id(input_data['from_passage_id']).type_id,
            'to_passage_id': from_global_id(input_data['to_passage_id']).type_id,
        })
        serializer.is_valid(raise_exception=True)
        choice = serializer.save()
        return cls(choice=choice)


class Mutation(graphene.ObjectType):
    create_choice = CreateChoice.Field()
    update_choice = UpdateChoice.Field()
