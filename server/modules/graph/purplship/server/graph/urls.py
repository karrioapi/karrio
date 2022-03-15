"""
karrio server graph module urls
"""
import pydoc
import typing
from django.conf import settings
from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from graphene_django.views import GraphQLView as BaseGraphQLView
from rest_framework import exceptions

ACCESS_METHOD = getattr(
    settings,
    "SESSION_ACCESS_MIXIN",
    "karrio.server.core.authentication.AccessMixin",
)
AccessMixin: typing.Any = pydoc.locate(ACCESS_METHOD)


class GraphQLView(AccessMixin, BaseGraphQLView):
    @staticmethod
    def format_error(error):
        formatted_error = super(GraphQLView, GraphQLView).format_error(error)

        if hasattr(error, "original_error"):
            if isinstance(error.original_error, exceptions.APIException):
                formatted_error["message"] = str(error.original_error.detail)
                formatted_error["code"] = getattr(
                    error.original_error, "code", error.original_error.default_code
                )
                formatted_error["status_code"] = error.original_error.status_code

            if isinstance(error.original_error, exceptions.ValidationError):
                formatted_error["message"] = str(error.original_error.default_detail)
                formatted_error["validation"] = error.original_error.detail

        return formatted_error


app_name = "karrio.server.graph"
urlpatterns = [
    path("graphql", csrf_exempt(GraphQLView.as_view(graphiql=True)), name="graphql"),
]
