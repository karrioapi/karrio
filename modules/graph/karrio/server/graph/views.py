"""
karrio server graph module urls
"""

import pydoc
import typing
import logging
from django.urls import path
from django.conf import settings
from rest_framework import exceptions
from django.views.decorators.csrf import csrf_exempt
import graphql.error.graphql_error as graphql
import strawberry.django.views as views
import strawberry.types as types
import strawberry.http as http

import karrio.lib as lib
import karrio.server.conf as conf
import karrio.server.graph.schema as schema

logger = logging.getLogger(__name__)
ACCESS_METHOD = getattr(
    settings,
    "SESSION_ACCESS_MIXIN",
    "karrio.server.core.authentication.AccessMixin",
)
AccessMixin: typing.Any = pydoc.locate(ACCESS_METHOD)


class GraphQLView(AccessMixin, views.GraphQLView):
    def dispatch(self, request, *args, **kwargs):
        should_render_graphiql = lib.failsafe(
            lambda: self.should_render_graphiql(request)
        )

        if should_render_graphiql:
            context = dict(APP_NAME=conf.settings.APP_NAME)

            return self._render_graphiql(request, context=context)

        return super().dispatch(request, *args, **kwargs)

    def process_result(
        self, request, result: types.ExecutionResult
    ) -> http.GraphQLHTTPResponse:
        data: http.GraphQLHTTPResponse = {"data": result.data}

        if result.errors:
            data["errors"] = [self.format_graphql_error(err) for err in result.errors]
        if result.extensions:
            data["extensions"] = result.extensions

        return data

    def format_graphql_error(self, error: graphql.GraphQLError):
        formatted_error: dict = (
            graphql.format_error(error)  # type: ignore
            if isinstance(error, graphql.GraphQLError)
            else {}
        )

        if isinstance(error.original_error, exceptions.APIException):
            formatted_error["message"] = str(error.original_error.detail)
            formatted_error["code"] = (
                error.original_error.get_codes()
                if hasattr(error.original_error, "get_codes")
                else getattr(
                    error.original_error,
                    "code",
                    getattr(error.original_error, "default_code", None),
                )
            )
            formatted_error["status_code"] = error.original_error.status_code

        if isinstance(error.original_error, exceptions.ValidationError):
            formatted_error["message"] = str(error.original_error.default_detail)
            formatted_error["validation"] = error.original_error.detail

        return formatted_error


urlpatterns = [
    path(
        "graphql/",
        csrf_exempt(GraphQLView.as_view(schema=schema.schema)),
        name="graphql",
    ),
    path(
        "graphql",
        csrf_exempt(GraphQLView.as_view(schema=schema.schema)),
        name="graphql-api",
    ),
]
