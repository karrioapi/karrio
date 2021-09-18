"""
purplship server graph module urls
"""
from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from graphene_django.views import GraphQLView as BaseGraphQLView

from purpleserver.core.authentication import AllAuthentication


class GraphQLView(AllAuthentication, BaseGraphQLView):
    pass


app_name = 'purpleserver.graph'
urlpatterns = [
    path("graphql", csrf_exempt(GraphQLView.as_view(graphiql=True))),
]
