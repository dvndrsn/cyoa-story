import graphene


class CreateStory(graphene.ClientIDMutation):
    
    class Input:
        title = graphene.String()
        subtitle = graphene.String()
        description = graphene.String()

    story = graphene.Field('api.query.story.StoryType')

    @classmethod
    def mutate_and_get_payload(cls, info, **input_data):
        return cls(story=None)


class UpdateStory(graphene.ClientIDMutation):
    
    class Input:
        story_id = graphene.ID()
        title = graphene.String()
        subtitle = graphene.String()
        description = graphene.String()

    story = graphene.Field('api.query.story.StoryType')

    @classmethod
    def mutate_and_get_payload(cls, info, **input_data):
        return cls(story=None)


class Mutation(graphene.ObjectType):
    create_story = CreateStory.Field()
    update_story = UpdateStory.Field()
