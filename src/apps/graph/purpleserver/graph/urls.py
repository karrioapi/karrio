"""
purplship server manager module urls
"""
from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.mixins import LoginRequiredMixin

from graphene_django.views import GraphQLView


class PurplshipGraphQLView(LoginRequiredMixin, GraphQLView):
    pass


app_name = 'purpleserver.graph'
urlpatterns = [
    path("graphql", csrf_exempt(PurplshipGraphQLView.as_view(graphiql=True))),
]
