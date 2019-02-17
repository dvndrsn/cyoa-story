from graphene_django.views import GraphQLView as BaseGraphQLView

from .loaders import Loaders
from .schema import SCHEMA


class GraphQLView(BaseGraphQLView):
    def get_context(self, request):
        request.loaders = getattr(request, 'loaders', Loaders())
        return request


STORY_GRAPHQL_VIEW = GraphQLView.as_view(schema=SCHEMA, graphiql=True)
