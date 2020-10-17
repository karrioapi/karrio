import logging
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes, throttle_classes
from rest_framework.response import Response
from rest_framework.request import Request

from django.urls import path

from drf_yasg.utils import swagger_auto_schema

from purplship.core.utils import to_dict

from purpleserver.core.serializers import (
    TrackingRequest, TrackingResponse, TestFilters, ErrorResponse
)
from purpleserver.core.gateway import Shipments
from purpleserver.proxy.router import router

logger = logging.getLogger(__name__)
ENDPOINT_ID = "@@@"  # This endpoint id is used to make operation ids unique make sure not to duplicate

DESCRIPTIONS = """
**[proxy]**

You can track a shipment by specifying the carrier and the shipment tracking number.
"""


@swagger_auto_schema(
    methods=['get'],
    tags=['Tracking'],
    operation_id=f"{ENDPOINT_ID}fetch",
    operation_summary="Track a shipment",
    operation_description=DESCRIPTIONS,
    responses={200: TrackingResponse(), 400: ErrorResponse()},
    query_serializer=TestFilters
)
@api_view(['GET'])
@authentication_classes((SessionAuthentication, BasicAuthentication, TokenAuthentication))
@permission_classes((IsAuthenticated, ))
@throttle_classes([UserRateThrottle, AnonRateThrottle])
def track_shipment(request: Request, carrier_name: str, tracking_number: str):
    params = TestFilters(data=request.query_params)
    params.is_valid(raise_exception=True)

    tracking_request = TrackingRequest(data=dict(tracking_numbers=[tracking_number]))
    tracking_request.is_valid(raise_exception=True)

    response = Shipments.track(
        tracking_request.data,
        carrier_filter={**params.validated_data, 'carrier_name': carrier_name}
    )

    return Response(
        to_dict(response),
        status=status.HTTP_200_OK if response.tracking_details is not None else status.HTTP_404_NOT_FOUND
    )


router.urls.append(path('proxy/tracking/<carrier_name>/<tracking_number>', track_shipment, name="shipment-tracking"))
