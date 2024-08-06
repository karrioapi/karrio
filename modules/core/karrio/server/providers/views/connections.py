import logging
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

logger = logging.getLogger(__name__)
ENDPOINT_ID = "&&&"  # This endpoint id is used to make operation ids unique make sure not to duplicate
CarrierConnectionList = serializers.PaginatedResult(
    "CarrierConnectionList", serializers.CarrierConnection
)


class CarrierConnectionListView(api.GenericAPIView):
    model = models.Carrier
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

        # fmt: off
        connections = gateway.Carriers.list(**filter)
        response = self.paginate_queryset(
            [
                {
                    **_,
                    "metadata": None if _["is_system"] else _["metadata"],
                    "credentials": None if _["is_system"] else _["credentials"]
                }
                for _ in serializers.CarrierConnection(connections, many=True).data
            ]
        )
        # fmt: on

        return self.get_paginated_response(response)

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
        connection = models.Carrier.access_by(request).get(pk=pk)
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
        connection = models.Carrier.access_by(request).get(pk=pk)
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
        connection = models.Carrier.access_by(request).get(pk=pk)

        connection.delete(keep_parents=True)

        return response.Response(serializers.CarrierConnection(connection).data)


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
]
