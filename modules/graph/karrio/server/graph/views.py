"""
karrio server graph module urls
"""

import pydoc
import typing

import graphql.error.graphql_error as graphql
import karrio.lib as lib
import karrio.server.conf as conf
import karrio.server.graph.schema as schema
import strawberry.django.views as views
import strawberry.http as http
import strawberry.types as types
from django.conf import settings
from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from karrio.server.core.logging import logger
from rest_framework import exceptions

ACCESS_METHOD = getattr(
    settings,
    "SESSION_ACCESS_MIXIN",
    "karrio.server.core.authentication.AccessMixin",
)
AccessMixin: typing.Any = pydoc.locate(ACCESS_METHOD)


class GraphQLView(AccessMixin, views.GraphQLView):
    def dispatch(self, request, *args, **kwargs):
        should_render_graphiql = lib.failsafe(lambda: self.should_render_graphiql(request))

        if should_render_graphiql:
            context = dict(APP_NAME=conf.settings.APP_NAME)

            return self._render_graphiql(request, context=context)

        return super().dispatch(request, *args, **kwargs)

    def process_result(self, request, result: types.ExecutionResult) -> http.GraphQLHTTPResponse:
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

        elif isinstance(error.original_error, exceptions.ValidationError):
            formatted_error["message"] = str(error.original_error.default_detail)
            formatted_error["validation"] = error.original_error.detail

        elif error.original_error is not None:
            # Log unhandled exceptions so they reach Sentry instead of being
            # silently masked as generic INTERNAL_SERVER_ERROR responses.
            logger.error(
                "Unhandled GraphQL error: %s",
                error.original_error,
                exc_info=error.original_error,
            )

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
