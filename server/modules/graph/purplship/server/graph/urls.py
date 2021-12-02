"""
purplship server graph module urls
"""
from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from graphene_django.views import GraphQLView as BaseGraphQLView

from purplship.server.core.authentication import AllAuthentication


class GraphQLView(AllAuthentication, BaseGraphQLView):
    pass


app_name = "purplship.server.graph"
urlpatterns = [
    path("graphql", csrf_exempt(GraphQLView.as_view(graphiql=True)), name="graphql"),
]
