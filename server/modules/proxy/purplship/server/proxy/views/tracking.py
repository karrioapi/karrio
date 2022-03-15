import logging
from django.urls import path
from rest_framework import status
from rest_framework.response import Response
from rest_framework.request import Request
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from karrio.server.serializers import SerializerDecorator
from karrio.server.core.views.api import APIView
from karrio.server.core.serializers import (
    TrackingRequest, TrackingResponse, TestFilters, ErrorResponse, MODELS
)
from karrio.server.core.gateway import Shipments
from karrio.server.proxy.router import router

logger = logging.getLogger(__name__)
ENDPOINT_ID = "@@@@"  # This endpoint id is used to make operation ids unique make sure not to duplicate
CARRIER_NAMES = list(MODELS.keys())


class TrackingAPIView(APIView):
    logging_methods = ['GET']

    @swagger_auto_schema(
        tags=['Proxy'],
        operation_id=f"{ENDPOINT_ID}track_shipment",
        operation_summary="Track a shipment",
        query_serializer=TestFilters(),
        responses={200: TrackingResponse(), 400: ErrorResponse()},
        manual_parameters=[
            openapi.Parameter('carrier_name', in_=openapi.IN_PATH, type=openapi.TYPE_STRING, enum=CARRIER_NAMES),
        ],
    )
    def get(self, request: Request, carrier_name: str, tracking_number: str):
        """
        You can track a shipment by specifying the carrier and the shipment tracking number.
        """
        test_filter = SerializerDecorator[TestFilters](data=request.query_params).data
        payload = SerializerDecorator[TrackingRequest](data=dict(tracking_numbers=[tracking_number])).data

        response = Shipments.track(payload, context=request, carrier_name=carrier_name, **test_filter)

        return Response(
            TrackingResponse(response).data,
            status=status.HTTP_200_OK if response.tracking is not None else status.HTTP_404_NOT_FOUND
        )


router.urls.append(path('proxy/tracking/<carrier_name>/<tracking_number>', TrackingAPIView.as_view(), name="shipment-tracking"))
