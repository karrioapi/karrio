"""
karrio server graph module urls
"""
from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from karrio.server.graph.views import GraphQLView


app_name = "karrio.server.graph"
urlpatterns = [
    path("graphql", csrf_exempt(GraphQLView.as_view(graphiql=True)), name="graphql"),
]
