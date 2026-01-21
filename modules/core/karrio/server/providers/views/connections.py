import django.urls as urls
import rest_framework.status as status
import rest_framework.request as request
import rest_framework.response as response
import django_filters.rest_framework as drf
import rest_framework.pagination as pagination

import karrio.lib as lib
import karrio.server.openapi as openapi
import karrio.server.core.views.api as api
import karrio.server.core.filters as filters
import karrio.server.core.gateway as gateway
import karrio.server.providers.models as models
import karrio.server.providers.serializers as serializers

ENDPOINT_ID = "&&&"  # This endpoint id is used to make operation ids unique make sure not to duplicate
CarrierConnectionList = serializers.PaginatedResult(
    "CarrierConnectionList", serializers.CarrierConnection
)


class CarrierConnectionListView(api.GenericAPIView):
    model = models.CarrierConnection
    serializer_class = serializers.CarrierConnection
    filterset_class = filters.CarrierConnectionFilter
    filter_backends = (drf.DjangoFilterBackend,)
    pagination_class = type(
        "CustomPagination",
        (pagination.LimitOffsetPagination,),
        dict(default_limit=20),
    )

    @openapi.extend_schema(
        tags=["Connections"],
        operation_id=f"{ENDPOINT_ID}list",
        extensions={"x-operationId": "listCarrierConnections"},
        summary="List carrier connections",
        responses={
            200: CarrierConnectionList(),
            400: serializers.ErrorResponse(),
        },
        parameters=filters.CarrierConnectionFilter.parameters,
    )
    def get(self, request: request.Request):
        """Retrieve all carrier connections"""
        filter = {
            **filters.CarrierFilters(request.query_params).to_dict(),
            "context": request,
        }

        connections = gateway.Carriers.list(**filter)
        # Note: Credentials are no longer returned (write-only field)
        # Metadata is masked for system connections (BrokeredConnection)
        paginated = self.paginate_queryset(
            [
                {**_, "metadata": None if _["is_system"] else _["metadata"]}
                for _ in serializers.CarrierConnection(connections, many=True).data
            ]
        )

        return self.get_paginated_response(paginated)

    @openapi.extend_schema(
        tags=["Connections"],
        operation_id=f"{ENDPOINT_ID}add",
        extensions={"x-operationId": "addCarrierConnection"},
        summary="Add a carrier connection",
        responses={
            201: serializers.CarrierConnection(),
            400: serializers.ErrorResponse(),
            424: serializers.ErrorMessages(),
            500: serializers.ErrorResponse(),
        },
        request=serializers.CarrierConnectionData(),
    )
    def post(self, request: request.Request):
        """Add a new carrier connection."""
        connection = lib.identity(
            serializers.CarrierConnectionModelSerializer.map(
                data=serializers.CarrierConnectionData.map(data=request.data).data,
                context=request,
            )
            .save()
            .instance
        )

        return response.Response(
            serializers.CarrierConnection(connection).data,
            status=status.HTTP_201_CREATED,
        )


class CarrierConnectionDetail(api.APIView):
    @openapi.extend_schema(
        tags=["Connections"],
        operation_id=f"{ENDPOINT_ID}retrieve",
        extensions={"x-operationId": "retrieveCarrierConnection"},
        summary="Retrieve a connection",
        responses={
            200: serializers.CarrierConnection(),
            400: serializers.ErrorResponse(),
            500: serializers.ErrorResponse(),
        },
    )
    def get(self, request: request.Request, pk: str):
        """Retrieve carrier connection."""
        connection = models.CarrierConnection.access_by(request).get(pk=pk)
        return response.Response(serializers.CarrierConnection(connection).data)

    @openapi.extend_schema(
        tags=["Connections"],
        operation_id=f"{ENDPOINT_ID}update",
        extensions={"x-operationId": "updateCarrierConnection"},
        summary="Update a connection",
        request=serializers.CarrierConnectionData(),
        responses={
            200: serializers.CarrierConnection(),
            400: serializers.ErrorResponse(),
            404: serializers.ErrorResponse(),
            500: serializers.ErrorResponse(),
        },
    )
    def patch(self, request: request.Request, pk: str):
        """Update a carrier connection."""
        connection = models.CarrierConnection.access_by(request).get(pk=pk)
        update = lib.identity(
            serializers.CarrierConnectionModelSerializer.map(
                connection,
                data=request.data,
                context=request,
            )
            .save()
            .instance
        )

        return response.Response(serializers.CarrierConnection(update).data)

    @openapi.extend_schema(
        tags=["Connections"],
        operation_id=f"{ENDPOINT_ID}remove",
        extensions={"x-operationId": "removeCarrierConnection"},
        summary="Remove a carrier connection",
        responses={
            200: serializers.CarrierConnection(),
            404: serializers.ErrorResponse(),
            409: serializers.ErrorResponse(),
            500: serializers.ErrorResponse(),
        },
    )
    def delete(self, request: request.Request, pk: str):
        """Remove a carrier connection."""
        connection = models.CarrierConnection.access_by(request).get(pk=pk)

        connection.delete(keep_parents=True)

        return response.Response(serializers.CarrierConnection(connection).data)


class ConnectionWebhookRegister(api.APIView):
    @openapi.extend_schema(
        exclude=True,
        tags=["Connections"],
        operation_id=f"{ENDPOINT_ID}webhook-register",
        extensions={"x-operationId": "webhookRegister"},
        summary="Register a webhook for a carrier connection",
        request=serializers.WebhookRegisterData(),
        responses={
            200: serializers.WebhookOperationResponse(),
            400: serializers.ErrorResponse(),
            424: serializers.ErrorMessages(),
        },
    )
    def post(self, request: request.Request, pk: str):
        """Register a webhook endpoint for a carrier connection."""
        connection = models.CarrierConnection.access_by(request).get(pk=pk)
        webhook_url = request.build_absolute_uri(f"/v1/connections/webhook/{pk}/events")

        webhook_details = (
            serializers.WebhookRegisterSerializer.map(
                connection,
                data={"webhook_url": webhook_url, **request.data},
                context=request,
            )
            .save()
            .instance
        )

        updated = lib.identity(
            serializers.CarrierConnectionModelSerializer.map(
                connection,
                data=dict(
                    config=dict(
                        webhook_id=webhook_details.webhook_identifier,
                        webhook_secret=webhook_details.secret,
                        webhook_url=webhook_url,
                    )
                ),
                context=request,
            )
            .save()
            .instance
        )

        return response.Response(
            serializers.WebhookOperationResponse(
                dict(
                    carrier_name=updated.carrier_name,
                    carrier_id=updated.carrier_id,
                    operation="Webhook registration",
                    success=True,
                )
            ).data,
            status=status.HTTP_200_OK,
        )


class ConnectionWebhookDeregister(api.APIView):
    @openapi.extend_schema(
        exclude=True,
        tags=["Connections"],
        operation_id=f"{ENDPOINT_ID}webhook-deregister",
        extensions={"x-operationId": "webhookDeregister"},
        summary="Deregister a webhook for a carrier connection",
        responses={
            200: serializers.WebhookOperationResponse(),
            400: serializers.ErrorResponse(),
            424: serializers.ErrorMessages(),
        },
    )
    def post(self, request: request.Request, pk: str):
        """Deregister a webhook endpoint from a carrier connection."""
        connection = models.CarrierConnection.access_by(request).get(pk=pk)

        serializers.WebhookDeregisterSerializer.map(
            connection,
            data=dict(webhook_id=connection.config.get("webhook_id")),
            context=request,
        ).save()

        updated = lib.identity(
            serializers.CarrierConnectionModelSerializer.map(
                connection,
                data=dict(
                    config=dict(
                        webhook_id=None,
                        webhook_secret=None,
                        webhook_url=None,
                    )
                ),
                context=request,
            )
            .save()
            .instance
        )

        return response.Response(
            serializers.WebhookOperationResponse(
                dict(
                    operation="Webhook deregistration",
                    success=True,
                    carrier_name=updated.carrier_name,
                    carrier_id=updated.carrier_id,
                )
            ).data,
            status=status.HTTP_200_OK,
        )


class ConnectionWebhookDisconnect(api.APIView):
    @openapi.extend_schema(
        exclude=True,
        tags=["Connections"],
        operation_id=f"{ENDPOINT_ID}webhook-disconnect",
        extensions={"x-operationId": "webhookDisconnect"},
        summary="Force disconnect a webhook for a carrier connection",
        responses={
            200: serializers.WebhookOperationResponse(),
            400: serializers.ErrorResponse(),
        },
    )
    def post(self, request: request.Request, pk: str):
        """Force disconnect a webhook from a carrier connection (local only)."""
        connection = models.CarrierConnection.access_by(request).get(pk=pk)

        updated = lib.identity(
            serializers.CarrierConnectionModelSerializer.map(
                connection,
                data=dict(
                    config=dict(
                        webhook_id=None,
                        webhook_secret=None,
                        webhook_url=None,
                    )
                ),
                context=request,
            )
            .save()
            .instance
        )

        return response.Response(
            serializers.WebhookOperationResponse(
                dict(
                    operation="Webhook disconnect",
                    success=True,
                    carrier_name=updated.carrier_name,
                    carrier_id=updated.carrier_id,
                )
            ).data,
            status=status.HTTP_200_OK,
        )


class ConnectionWebhookEvent(api.APIView):
    """Handle inbound webhook events from carriers."""

    throttle_classes: list = []
    permission_classes: list = []
    authentication_classes: list = []

    @openapi.extend_schema(
        exclude=True,
        tags=["Connections"],
        operation_id=f"{ENDPOINT_ID}webhook-event",
        extensions={"x-operationId": "webhookEvent"},
        summary="Handle carrier webhook events",
        responses={
            200: serializers.OperationConfirmation(),
        },
    )
    def post(self, request: request.Request, pk: str):
        """Handle inbound webhook events from a carrier via POST."""
        data, http_status = serializers.WebhookEventSerializer.process_event(
            request, pk
        )
        return response.Response(data, status=http_status)


class ConnectionOauthAuthorize(api.APIView):
    @openapi.extend_schema(
        exclude=True,
        tags=["Connections"],
        operation_id=f"{ENDPOINT_ID}oauth-authorize",
        extensions={"x-operationId": "oauthAuthorize"},
        summary="Handle an OAuth authorize",
        request=serializers.OAuthAuthorizeData(),
    )
    def post(self, request: request.Request, carrier_name: str):
        """Handle an OAuth authorize."""

        [output, messages] = gateway.Hooks.on_oauth_authorize(
            serializers.OAuthAuthorizeData.map(
                data={
                    "redirect_uri": request.build_absolute_uri(
                        f"/v1/connections/oauth/{carrier_name}/callback"
                    ),
                    **request.data,
                }
            ).data,
            carrier_name=carrier_name,
            test_mode=request.test_mode,
        )

        # Include the frontend_url for the callback to redirect to
        frontend_url = request.data.get("frontend_url")

        return response.Response(
            dict(
                operation="OAuth authorize",
                request=lib.to_dict(output),
                messages=lib.to_dict(messages),
                frontend_url=frontend_url,
            ),
            status=status.HTTP_200_OK,
        )


class ConnectionOauthCallback(api.APIView):
    @openapi.extend_schema(
        exclude=True,
        tags=["Connections"],
        operation_id=f"{ENDPOINT_ID}oauth-callback",
        extensions={"x-operationId": "oauthCallback"},
        summary="Handle an OAuth callback",
        request=serializers.OAuthCallbackData(),
        responses={
            200: serializers.OperationConfirmation(),
        },
    )
    def get(self, request: request.Request, carrier_name: str):
        """Handle an OAuth callback via GET."""
        return self._handle_callback(request, carrier_name)

    @openapi.extend_schema(
        exclude=True,
        tags=["Connections"],
        operation_id=f"{ENDPOINT_ID}oauth-callback-post",
        extensions={"x-operationId": "oauthCallbackPost"},
        summary="Handle an OAuth callback via POST",
        request=serializers.OAuthCallbackData(),
        responses={
            200: serializers.OperationConfirmation(),
        },
    )
    def post(self, request: request.Request, carrier_name: str):
        """Handle an OAuth callback via POST."""
        return self._handle_callback(request, carrier_name)

    def _handle_callback(self, request: request.Request, carrier_name: str):
        """Handle OAuth callback processing.

        Returns JSON with OAuth result for the frontend to process.
        When called from a browser popup, renders template or redirects to frontend.
        """
        import json
        import base64
        from django.shortcuts import render
        from django.http import HttpResponseRedirect

        result, frontend_url = serializers.OAuthCallbackSerializer.process_callback(
            request, carrier_name
        )

        accept_header = request.headers.get("Accept", "")

        if "text/html" in accept_header and frontend_url:
            result_encoded = base64.b64encode(
                json.dumps(result).encode("utf-8")
            ).decode("utf-8")
            return HttpResponseRedirect(f"{frontend_url}?oauth_result={result_encoded}")

        if "text/html" in accept_header:
            error_message = (
                result["messages"][0]["message"]
                if result["messages"]
                else "An error occurred during authorization."
            )
            return render(
                request._request,
                "providers/oauth_callback.html",
                dict(
                    success=result["success"],
                    error_message=error_message,
                    result_json=json.dumps(result),
                ),
            )

        return response.Response(result, status=status.HTTP_200_OK)


urlpatterns = [
    urls.path(
        "connections",
        CarrierConnectionListView.as_view(),
        name="carrier-connection-list",
    ),
    urls.path(
        "connections/<str:pk>",
        CarrierConnectionDetail.as_view(),
        name="carrier-connection-details",
    ),
    urls.path(
        "connections/oauth/<str:carrier_name>/authorize",
        ConnectionOauthAuthorize.as_view(),
        name="connection-oauth-authorize",
    ),
    urls.path(
        "connections/oauth/<str:carrier_name>/callback",
        ConnectionOauthCallback.as_view(),
        name="connection-oauth-callback",
    ),
    urls.path(
        "connections/webhook/<str:pk>/events",
        ConnectionWebhookEvent.as_view(),
        name="connection-webhook-event",
    ),
    urls.path(
        "connections/webhook/<str:pk>/register",
        ConnectionWebhookRegister.as_view(),
        name="connection-webhook-register",
    ),
    urls.path(
        "connections/webhook/<str:pk>/deregister",
        ConnectionWebhookDeregister.as_view(),
        name="connection-webhook-deregister",
    ),
    urls.path(
        "connections/webhook/<str:pk>/disconnect",
        ConnectionWebhookDisconnect.as_view(),
        name="connection-webhook-disconnect",
    ),
]
