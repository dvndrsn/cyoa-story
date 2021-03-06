from typing import Any

import graphene

from api.utils import from_global_id
from story.services import AuthorService


class CreateAuthor(graphene.ClientIDMutation):

    class Input:
        first_name = graphene.String()
        last_name = graphene.String()
        twitter_account = graphene.String()

    author = graphene.Field('api.query.author.AuthorType')

    @classmethod
    def mutate_and_get_payload(cls, root: Any, info: graphene.ResolveInfo, **input_data: dict) -> 'CreateAuthor':
        serializer = AuthorService(data={
            'first_name': input_data['first_name'],
            'last_name': input_data['last_name'],
            'twitter_account': input_data['twitter_account'],
        })
        serializer.is_valid(raise_exception=True)
        author = serializer.save()
        return cls(author=author)


class UpdateAuthor(graphene.ClientIDMutation):

    class Input:
        author_id = graphene.ID()
        first_name = graphene.String()
        last_name = graphene.String()
        twitter_account = graphene.String()

    author = graphene.Field('api.query.author.AuthorType')

    @classmethod
    def mutate_and_get_payload(cls, root: Any, info: graphene.ResolveInfo, **input_data: dict) -> 'UpdateAuthor':
        author = from_global_id(input_data['author_id'])
        serializer = AuthorService.for_instance(author.type_id, data={
            'first_name': input_data['first_name'],
            'last_name': input_data['last_name'],
            'twitter_account': input_data['twitter_account'],
        })
        serializer.is_valid(raise_exception=True)
        author = serializer.save()
        return cls(author=author)


class Mutation(graphene.ObjectType):
    create_author = CreateAuthor.Field()
    update_author = UpdateAuthor.Field()
