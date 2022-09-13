import logging
from django.urls import path
from rest_framework import status
from rest_framework.response import Response
from rest_framework.request import Request
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

import karrio.server.serializers as serializers
import karrio.server.providers.models as providers
from karrio.server.proxy.router import router
from karrio.server.core.gateway import Pickups
from karrio.server.core.views.api import APIView
from karrio.server.core.serializers import (
    PickupCancelRequest,
    PickupUpdateRequest,
    OperationResponse,
    PickupResponse,
    PickupRequest,
    ErrorResponse,
    ErrorMessages,
)

logger = logging.getLogger(__name__)
ENDPOINT_ID = "@"  # This endpoint id is used to make operation ids unique make sure not to duplicate
CARRIER_NAMES = list(providers.MODELS.keys())


class PickupSchedule(APIView):
    @swagger_auto_schema(
        tags=["Proxy"],
        operation_id=f"{ENDPOINT_ID}schedule_pickup",
        operation_summary="Schedule a pickup",
        request_body=PickupRequest(),
        responses={
            201: PickupResponse(),
            400: ErrorResponse(),
            424: ErrorMessages(),
            500: ErrorResponse(),
        },
        manual_parameters=[
            openapi.Parameter(
                "carrier_name",
                in_=openapi.IN_PATH,
                type=openapi.TYPE_STRING,
                enum=CARRIER_NAMES,
            ),
        ],
    )
    def post(self, request: Request, carrier_name: str):
        """
        Schedule one or many parcels pickup
        """
        payload = serializers.SerializerDecorator[PickupRequest](data=request.data).data

        response = Pickups.schedule(payload, context=request, carrier_name=carrier_name)

        return Response(PickupResponse(response).data, status=status.HTTP_201_CREATED)


class PickupUpdate(APIView):
    @swagger_auto_schema(
        tags=["Proxy"],
        operation_id=f"{ENDPOINT_ID}update_pickup",
        operation_summary="Update a pickup",
        request_body=PickupUpdateRequest(),
        responses={
            200: PickupResponse(),
            400: ErrorResponse(),
            424: ErrorMessages(),
            500: ErrorResponse(),
        },
        manual_parameters=[
            openapi.Parameter(
                "carrier_name",
                in_=openapi.IN_PATH,
                type=openapi.TYPE_STRING,
                enum=CARRIER_NAMES,
            ),
        ],
    )
    def post(self, request: Request, carrier_name: str):
        """
        Modify a scheduled pickup
        """
        payload = serializers.SerializerDecorator[PickupUpdateRequest](data=request.data).data

        response = Pickups.update(payload, context=request, carrier_name=carrier_name)

        return Response(PickupResponse(response).data, status=status.HTTP_200_OK)


class PickupCancel(APIView):
    @swagger_auto_schema(
        tags=["Proxy"],
        operation_id=f"{ENDPOINT_ID}cancel_pickup",
        operation_summary="Cancel a pickup",
        request_body=PickupCancelRequest(),
        responses={
            200: OperationResponse(),
            400: ErrorResponse(),
            424: ErrorMessages(),
            500: ErrorResponse(),
        },
        manual_parameters=[
            openapi.Parameter(
                "carrier_name",
                in_=openapi.IN_PATH,
                type=openapi.TYPE_STRING,
                enum=CARRIER_NAMES,
            ),
        ],
    )
    def post(self, request: Request, carrier_name: str):
        """
        Cancel a pickup previously scheduled
        """
        payload = serializers.SerializerDecorator[PickupCancelRequest](data=request.data).data

        response = Pickups.cancel(payload, context=request, carrier_name=carrier_name)

        return Response(OperationResponse(response).data, status=status.HTTP_200_OK)


router.urls.append(
    path(
        "proxy/pickups/<carrier_name>", PickupSchedule.as_view(), name="pickup-schedule"
    )
)
router.urls.append(
    path(
        "proxy/pickups/<carrier_name>/update",
        PickupUpdate.as_view(),
        name="pickup-details",
    )
)
router.urls.append(
    path(
        "proxy/pickups/<carrier_name>/cancel",
        PickupCancel.as_view(),
        name="pickup-cancel",
    )
)
