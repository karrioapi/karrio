"""
karrio server graph module urls
"""
import pydoc
import typing
from django.urls import path
from django.conf import settings

import strawberry.http as http
import strawberry.types as types
import strawberry.django.views as views

import karrio.server.graph.schema as schema

ACCESS_METHOD = getattr(
    settings,
    "SESSION_ACCESS_MIXIN",
    "karrio.server.core.authentication.AccessMixin",
)
AccessMixin: typing.Any = pydoc.locate(ACCESS_METHOD)


class GraphQLView(AccessMixin, views.GraphQLView):
    def process_result(self, request, result: types.ExecutionResult) -> http.GraphQLHTTPResponse:
        data: http.GraphQLHTTPResponse = {"data": result.data}

        if result.errors:
            data["errors"] = [format_graphql_error(err) for err in result.errors]

        return data


def format_graphql_error(error):
    return error


urlpatterns = [
    path("graphql/", GraphQLView.as_view(schema=schema.schema), name="graphql"),
]
