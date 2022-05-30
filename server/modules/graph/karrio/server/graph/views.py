from django.urls import path
from strawberry.django.views import GraphQLView

from karrio.server.graph.schemas import schema

urlpatterns = [
    path("graphql/", GraphQLView.as_view(schema=schema), name="graphql"),
]
