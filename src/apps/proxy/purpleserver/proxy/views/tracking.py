import logging
from django.urls import path
from rest_framework import status
from rest_framework.response import Response
from rest_framework.request import Request
from drf_yasg.utils import swagger_auto_schema

from purpleserver.core.views.api import APIView
from purpleserver.core.serializers import (
    TrackingRequest, TrackingResponse, TestFilters, ErrorResponse
)
from purpleserver.core.gateway import Shipments
from purpleserver.proxy.router import router

logger = logging.getLogger(__name__)
ENDPOINT_ID = "@@@@"  # This endpoint id is used to make operation ids unique make sure not to duplicate


class TrackingAPIView(APIView):
    logging_methods = ['GET']

    @swagger_auto_schema(
        tags=['Proxy'],
        operation_id=f"{ENDPOINT_ID}track_shipment",
        operation_summary="Track a shipment",
        query_serializer=TestFilters(),
        responses={200: TrackingResponse(), 400: ErrorResponse()}
    )
    def get(self, request: Request, carrier_name: str, tracking_number: str):
        """
        You can track a shipment by specifying the carrier and the shipment tracking number.
        """
        params = TestFilters(data=request.query_params)
        params.is_valid(raise_exception=True)

        tracking_request = TrackingRequest(data=dict(tracking_numbers=[tracking_number]))
        tracking_request.is_valid(raise_exception=True)

        response = Shipments.track(
            tracking_request.data,
            carrier_filter={**params.validated_data, 'carrier_name': carrier_name, 'created_by': request.user}
        )

        return Response(
            TrackingResponse(response).data,
            status=status.HTTP_200_OK if response.tracking is not None else status.HTTP_404_NOT_FOUND
        )


router.urls.append(path('proxy/tracking/<carrier_name>/<tracking_number>', TrackingAPIView.as_view(), name="shipment-tracking"))
