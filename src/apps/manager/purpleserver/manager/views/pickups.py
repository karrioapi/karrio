import logging

from rest_framework import status
from rest_framework.response import Response
from rest_framework.request import Request

from django.urls import path
from drf_yasg.utils import swagger_auto_schema

from purpleserver.core.views.api import GenericAPIView
from purpleserver.core.serializers import (
    Pickup,
    ErrorResponse,
    OperationConfirmation,
    TestFilters,
)
from purpleserver.core.utils import SerializerDecorator
from purpleserver.manager.router import router
from purpleserver.manager.serializers import PickupData, PickupUpdateData, PickupCancelData

logger = logging.getLogger(__name__)
ENDPOINT_ID = "$$$$$"  # This endpoint id is used to make operation ids unique make sure not to duplicate


class PickupList(GenericAPIView):

    @swagger_auto_schema(
        tags=['Shipments'],
        operation_id=f"{ENDPOINT_ID}pickups",
        operation_summary="List shipment pickups",
        responses={200: Pickup(many=True), 400: ErrorResponse()}
    )
    def get(self, request: Request):
        """
        Retrieve all scheduled pickups.
        """
        pickups = request.user.pickup_set.all()

        response = self.paginate_queryset(Pickup(pickups, many=True).data)
        return Response(response)


class PickupRequest(GenericAPIView):

    @swagger_auto_schema(
        tags=['Shipments'],
        operation_id=f"{ENDPOINT_ID}schedule_pickup",
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
            "carrier_name": carrier_name
        }

        pickup = SerializerDecorator[PickupData](
            data=request.data).save(user=request.user, carrier_filter=carrier_filter).instance

        return Response(Pickup(pickup).data, status=status.HTTP_201_CREATED)


class PickupDetails(GenericAPIView):

    @swagger_auto_schema(
        tags=['Shipments'],
        operation_id=f"{ENDPOINT_ID}retrieve_pickup",
        operation_summary="Retrieve a pickup",
        responses={200: Pickup(), 400: ErrorResponse()},
    )
    def get(self, request: Request, pk: str):
        """Retrieve a scheduled pickup."""
        pickup = request.user.pickup_set.get(pk=pk)
        return Response(Pickup(pickup).data)

    @swagger_auto_schema(
        tags=['Shipments'],
        operation_id=f"{ENDPOINT_ID}update_pickup",
        operation_summary="Update a pickup",
        responses={200: OperationConfirmation(), 400: ErrorResponse()},
        request_body=PickupUpdateData()
    )
    def patch(self, request: Request, pk: str):
        """
        Modify a pickup for one or many shipments with labels already purchased.
        """
        pickup = request.user.pickup_set.get(pk=pk)
        instance = SerializerDecorator[PickupUpdateData](
            pickup, data=request.data).save(user=request.user).instance

        return Response(Pickup(instance).data, status=status.HTTP_200_OK)


class PickupCancel(GenericAPIView):

    @swagger_auto_schema(
        tags=['Shipments'],
        operation_id=f"{ENDPOINT_ID}cancel_pickup",
        operation_summary="Cancel a pickup",
        responses={200: OperationConfirmation(), 400: ErrorResponse()},
        request_body=PickupCancelData()
    )
    def post(self, request: Request, pk: str):
        """
        Cancel a pickup of one or more shipments.
        """
        pickup = request.user.pickup_set.get(pk=pk)
        confirmation = SerializerDecorator[PickupCancelData](
            pickup, data=request.data).save().instance

        return Response(OperationConfirmation(confirmation).data, status=status.HTTP_200_OK)


router.urls.append(path('shipment_pickups', PickupList.as_view(), name="shipment-pickup-list"))
router.urls.append(path('shipment_pickups/<str:pk>', PickupDetails.as_view(), name="shipment-pickup-details"))
router.urls.append(path('shipment_pickups/<str:pk>/cancel', PickupCancel.as_view(), name="shipment-pickup-cancel"))
router.urls.append(path('shipment_pickups/<str:carrier_name>/schedule', PickupRequest.as_view(), name="shipment-pickup-request"))
