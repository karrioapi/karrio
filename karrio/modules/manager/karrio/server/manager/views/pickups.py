import logging

from django.urls import path
from rest_framework import status
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.request import Request
from django_filters.rest_framework import DjangoFilterBackend

from karrio.server.core.views.api import GenericAPIView, APIView
from karrio.server.core.filters import PickupFilters
from karrio.server.manager.router import router
from karrio.server.manager.serializers import (
    PaginatedResult,
    Pickup,
    ErrorResponse,
    ErrorMessages,
    PickupData,
    PickupUpdateData,
    PickupCancelData,
)
import karrio.server.manager.models as models
import karrio.server.openapi as openapi

ENDPOINT_ID = "$$$$"  # This endpoint id is used to make operation ids unique make sure not to duplicate
logger = logging.getLogger(__name__)
Pickups = PaginatedResult("PickupList", Pickup)


class PickupList(GenericAPIView):
    pagination_class = type(
        "CustomPagination", (LimitOffsetPagination,), dict(default_limit=20)
    )
    filter_backends = (DjangoFilterBackend,)
    filterset_class = PickupFilters
    serializer_class = Pickups
    model = models.Pickup

    @openapi.extend_schema(
        tags=["Pickups"],
        operation_id=f"{ENDPOINT_ID}list",
        extensions={"x-operationId": "listPickups"},
        summary="List shipment pickups",
        responses={
            200: Pickups(),
            404: ErrorResponse(),
            500: ErrorResponse(),
        },
        parameters=PickupFilters.parameters,
    )
    def get(self, request: Request):
        """
        Retrieve all scheduled pickups.
        """
        pickups = self.filter_queryset(self.get_queryset())
        response = self.paginate_queryset(Pickup(pickups, many=True).data)
        return self.get_paginated_response(response)


class PickupRequest(APIView):
    throttle_scope = "carrier_request"

    @openapi.extend_schema(
        tags=["Pickups"],
        operation_id=f"{ENDPOINT_ID}schedule",
        extensions={"x-operationId": "schedulePickup"},
        summary="Schedule a pickup",
        responses={
            201: Pickup(),
            400: ErrorResponse(),
            424: ErrorMessages(),
            500: ErrorResponse(),
        },
        request=PickupData(),
    )
    def post(self, request: Request, carrier_name: str):
        """
        Schedule a pickup for one or many shipments with labels already purchased.
        """
        carrier_filter = {
            "carrier_name": carrier_name,
        }

        pickup = (
            PickupData.map(data=request.data, context=request)
            .save(carrier_filter=carrier_filter)
            .instance
        )

        return Response(Pickup(pickup).data, status=status.HTTP_201_CREATED)


class PickupDetails(APIView):
    throttle_scope = "carrier_request"

    @openapi.extend_schema(
        tags=["Pickups"],
        operation_id=f"{ENDPOINT_ID}retrieve",
        extensions={"x-operationId": "retrievePickup"},
        summary="Retrieve a pickup",
        responses={
            200: Pickup(),
            404: ErrorResponse(),
            500: ErrorResponse(),
        },
    )
    def get(self, request: Request, pk: str):
        """Retrieve a scheduled pickup."""
        pickup = models.Pickup.access_by(request).get(pk=pk)
        return Response(Pickup(pickup).data)

    @openapi.extend_schema(
        tags=["Pickups"],
        operation_id=f"{ENDPOINT_ID}update",
        extensions={"x-operationId": "updatePickup"},
        summary="Update a pickup",
        responses={
            200: Pickup(),
            404: ErrorResponse(),
            400: ErrorResponse(),
            424: ErrorMessages(),
            500: ErrorResponse(),
        },
        request=PickupUpdateData(),
    )
    def post(self, request: Request, pk: str):
        """
        Modify a pickup for one or many shipments with labels already purchased.
        """
        pickup = models.Pickup.access_by(request).get(pk=pk)
        instance = (
            PickupUpdateData.map(pickup, data=request.data, context=request)
            .save()
            .instance
        )

        return Response(Pickup(instance).data, status=status.HTTP_200_OK)


class PickupCancel(APIView):

    @openapi.extend_schema(
        tags=["Pickups"],
        operation_id=f"{ENDPOINT_ID}cancel",
        extensions={"x-operationId": "cancelPickup"},
        summary="Cancel a pickup",
        responses={
            200: Pickup(),
            404: ErrorResponse(),
            409: ErrorResponse(),
            424: ErrorMessages(),
            500: ErrorResponse(),
        },
        request=PickupCancelData(),
    )
    def post(self, request: Request, pk: str):
        """
        Cancel a pickup of one or more shipments.
        """
        pickup = models.Pickup.access_by(request).get(pk=pk)

        update = PickupCancelData.map(pickup, data=request.data).save().instance

        return Response(Pickup(update).data)


router.urls.append(path("pickups", PickupList.as_view(), name="shipment-pickup-list"))
router.urls.append(
    path("pickups/<str:pk>", PickupDetails.as_view(), name="shipment-pickup-details")
)
router.urls.append(
    path(
        "pickups/<str:pk>/cancel", PickupCancel.as_view(), name="shipment-pickup-cancel"
    )
)
router.urls.append(
    path(
        "pickups/<str:carrier_name>/schedule",
        PickupRequest.as_view(),
        name="shipment-pickup-request",
    )
)
