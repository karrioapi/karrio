import logging
from django.urls import path
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.request import Request

from purpleserver.core.views.api import GenericAPIView
from purpleserver.proxy.router import router
from purpleserver.core.utils import SerializerDecorator
from purpleserver.core.gateway import Pickups
from purpleserver.core.serializers import (
    PickupCancelRequest,
    PickupUpdateRequest,
    OperationResponse,
    PickupResponse,
    PickupRequest,
    ErrorResponse,
    TestFilters,
)

logger = logging.getLogger(__name__)
ENDPOINT_ID = "@@@@"  # This endpoint id is used to make operation ids unique make sure not to duplicate


class PickupDetails(GenericAPIView):

    @swagger_auto_schema(
        tags=['Pickups'],
        operation_id=f"{ENDPOINT_ID}schedule",
        operation_summary="Schedule a pickup",
        operation_description=(
            "**[proxy]**"
            "\n\n"
            "Schedule one or many parcels pickup"
        ),
        request_body=PickupRequest(),
        responses={200: PickupResponse(), 400: ErrorResponse()},
    )
    def post(self, request: Request, carrier_name: str):
        filters = SerializerDecorator[TestFilters](data=request.query_params).data
        payload = SerializerDecorator[PickupRequest](data=request.data).data

        response = Pickups.schedule(payload, carrier_filter={**filters, 'carrier_name': carrier_name})

        return Response(PickupResponse(response).data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        tags=['Pickups'],
        operation_id=f"{ENDPOINT_ID}update",
        operation_summary="Update a pickup",
        operation_description=(
            "**[proxy]**"
            "\n\n"
            "Modify a scheduled pickup"
        ),
        request_body=PickupUpdateRequest(),
        responses={200: PickupResponse(), 400: ErrorResponse()},
    )
    def put(self, request: Request, carrier_name: str):
        filters = SerializerDecorator[TestFilters](data=request.query_params).data
        payload = SerializerDecorator[PickupUpdateRequest](data=request.data).data

        response = Pickups.update(payload, carrier_filter={**filters, 'carrier_name': carrier_name})

        return Response(PickupResponse(response).data, status=status.HTTP_200_OK)


class PickupCancel(GenericAPIView):

    @swagger_auto_schema(
        tags=['Pickups'],
        operation_id=f"{ENDPOINT_ID}cancel",
        operation_summary="Cancel a pickup",
        operation_description=(
            "**[proxy]**"
            "\n\n"
            "Cancel a pickup previously scheduled"
        ),
        request_body=PickupCancelRequest(),
        responses={200: OperationResponse(), 400: ErrorResponse()},
    )
    def post(self, request: Request, carrier_name: str):
        filters = SerializerDecorator[TestFilters](data=request.query_params).data
        payload = SerializerDecorator[PickupCancelRequest](data=request.data).data

        response = Pickups.cancel(payload, carrier_filter={**filters, 'carrier_name': carrier_name})

        return Response(OperationResponse(response).data, status=status.HTTP_202_ACCEPTED)


router.urls.append(path('proxy/pickups/<carrier_name>', PickupDetails.as_view(), name="pickup-details"))
router.urls.append(path('proxy/pickups/<carrier_name>/cancel', PickupCancel.as_view(), name="pickup-cancel"))
