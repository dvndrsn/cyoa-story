from django.test import TestCase
import graphene

from api.query.author import Query, AuthorType
from api.query.story import StoryType
from api.tests.util import connection_to_list, request_with_loaders
from api.util import to_global_id
from story.factories import StoryFactory, AuthorFactory


class TestStoryNodeQuery(TestCase):

    def setUp(self):
        self.schema = graphene.Schema(query=Query, types=(AuthorType,))
        self.request = request_with_loaders()

    def build_query_with_fields(self, *fields):
        query = '''
        query getAuthorNode($id: ID!) {
            author: node(id: $id) {
                ... on AuthorType {
                    %s
                }
            }
        }
        ''' % ' '.join(fields)
        return query

    def test_author_node_query__returns_empty_field_when_id_does_not_exist(self):
        query_string = self.build_query_with_fields('id')
        variables = {'id': to_global_id(AuthorType, 1)}

        result = self.schema.execute(query_string, context=self.request, variables=variables)

        self.assertEqual(result.errors, None)
        self.assertDictEqual(result.data, {'author': None})

    def test_author_node_query__returns_model_fields(self):
        AuthorFactory.create(
            id=3,
            first_name='Buddy',
            last_name='Holly',
            twitter_account='@buddy',
        )
        query_string = self.build_query_with_fields(
            'id',
            'firstName',
            'lastName',
            'twitterAccount',
        )
        variables = {'id': to_global_id(AuthorType, 3)}

        result = self.schema.execute(query_string, context=self.request, variables=variables)

        self.assertEqual(result.errors, None)
        self.assertDictEqual(result.data['author'], {
            'id': to_global_id(AuthorType, 3),
            'firstName': 'Buddy',
            'lastName': 'Holly',
            'twitterAccount': '@buddy',
        })

    def test_author_node_query__returns_related_stories(self):
        author = AuthorFactory(id=5)
        StoryFactory.create(id=2, author=author)
        StoryFactory.create(id=4, author=author)
        query_string = self.build_query_with_fields(
            'id',
            'stories { edges { node { id } } }',
        )
        variables = {'id': to_global_id(AuthorType, 5)}

        result = self.schema.execute(query_string, context=self.request, variables=variables)

        self.assertEqual(result.errors, None)
        self.assertEqual(connection_to_list(result.data['author']['stories']), [
            {'id': to_global_id(StoryType, 2)},
            {'id': to_global_id(StoryType, 4)},
        ])
