from graphene_django.views import GraphQLView as BaseGraphQLView

from .loaders import Loaders
from .schema import schema


class GraphQLView(BaseGraphQLView):
    def get_context(self, request):
        request.loaders = getattr(request, 'loaders',  Loaders())
        return request


story_graphql_view = GraphQLView.as_view(schema=schema, graphiql=True)
