import logging

from rest_framework import status, serializers
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.request import Request
from drf_yasg.utils import swagger_auto_schema
from django.urls import path

from purpleserver.core.views.api import GenericAPIView, APIView
from purpleserver.core.serializers import (
    FlagField,
    Pickup,
    ErrorResponse,
    OperationConfirmation,
    TestFilters,
)
from purpleserver.core.utils import SerializerDecorator, PaginatedResult
from purpleserver.manager.router import router
from purpleserver.manager.serializers import PickupData, PickupUpdateData, PickupCancelData
import purpleserver.manager.models as models

logger = logging.getLogger(__name__)
ENDPOINT_ID = "$$$$"  # This endpoint id is used to make operation ids unique make sure not to duplicate
Pickups = PaginatedResult('PickupList', Pickup)


class PickupFilters(serializers.Serializer):
    test_mode = FlagField(
        required=False, allow_null=True, default=None,
        help_text="This flag filter out pickup created from carriers in test or live mode")


class PickupList(GenericAPIView):
    serializer_class = Pickup
    queryset = models.Pickup.objects
    pagination_class = type('CustomPagination', (LimitOffsetPagination,), dict(default_limit=20))

    @swagger_auto_schema(
        tags=['Pickups'],
        operation_id=f"{ENDPOINT_ID}list",
        operation_summary="List shipment pickups",
        responses={200: Pickups(), 400: ErrorResponse()},
        query_serializer=PickupFilters
    )
    def get(self, request: Request):
        """
        Retrieve all scheduled pickups.
        """
        query = (
            SerializerDecorator[PickupFilters](data=request.query_params).data
            if any(request.query_params) else {}
        )
        pickups = models.Pickup.objects.access_with(request.user).filter(**query)

        response = self.paginate_queryset(Pickup(pickups, many=True).data)
        return self.get_paginated_response(response)


class PickupRequest(APIView):

    @swagger_auto_schema(
        tags=['Pickups'],
        operation_id=f"{ENDPOINT_ID}schedule",
        operation_summary="Schedule a pickup",
        responses={200: Pickup(), 400: ErrorResponse()},
        query_serializer=TestFilters(),
        request_body=PickupData()
    )
    def post(self, request: Request, carrier_name: str):
        """
        Schedule a pickup for one or many shipments with labels already purchased.
        """
        carrier_filter = {
            **SerializerDecorator[TestFilters](data=request.query_params).data,
            "carrier_name": carrier_name,
            "user": request.user
        }

        pickup = SerializerDecorator[PickupData](
            data=request.data, context_user=request.user).save(carrier_filter=carrier_filter).instance

        return Response(Pickup(pickup).data, status=status.HTTP_201_CREATED)


class PickupDetails(APIView):

    @swagger_auto_schema(
        tags=['Pickups'],
        operation_id=f"{ENDPOINT_ID}retrieve",
        operation_summary="Retrieve a pickup",
        responses={200: Pickup(), 400: ErrorResponse()},
    )
    def get(self, request: Request, pk: str):
        """Retrieve a scheduled pickup."""
        pickup = models.Pickup.objects.access_with(request.user).get(pk=pk)
        return Response(Pickup(pickup).data)

    @swagger_auto_schema(
        tags=['Pickups'],
        operation_id=f"{ENDPOINT_ID}update",
        operation_summary="Update a pickup",
        responses={200: OperationConfirmation(), 400: ErrorResponse()},
        request_body=PickupUpdateData()
    )
    def patch(self, request: Request, pk: str):
        """
        Modify a pickup for one or many shipments with labels already purchased.
        """
        pickup = models.Pickup.objects.access_with(request.user).get(pk=pk)
        instance = SerializerDecorator[PickupUpdateData](
            pickup, data=request.data, context_user=request.user).save().instance

        return Response(Pickup(instance).data, status=status.HTTP_200_OK)


class PickupCancel(APIView):

    @swagger_auto_schema(
        tags=['Pickups'],
        operation_id=f"{ENDPOINT_ID}cancel",
        operation_summary="Cancel a pickup",
        responses={200: OperationConfirmation(), 400: ErrorResponse()},
        request_body=PickupCancelData()
    )
    def post(self, request: Request, pk: str):
        """
        Cancel a pickup of one or more shipments.
        """
        pickup = models.Pickup.objects.access_with(request.user).get(pk=pk)
        confirmation = SerializerDecorator[PickupCancelData](
            pickup, data=request.data, context_user=request.user).save().instance

        return Response(OperationConfirmation(confirmation).data, status=status.HTTP_200_OK)


router.urls.append(path('pickups', PickupList.as_view(), name="shipment-pickup-list"))
router.urls.append(path('pickups/<str:pk>', PickupDetails.as_view(), name="shipment-pickup-details"))
router.urls.append(path('pickups/<str:pk>/cancel', PickupCancel.as_view(), name="shipment-pickup-cancel"))
router.urls.append(path('pickups/<str:carrier_name>/schedule', PickupRequest.as_view(), name="shipment-pickup-request"))
