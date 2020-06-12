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

from purpleserver.core.datatypes import ErrorResponse
from purpleserver.core.exceptions import ValidationError
from purpleserver.core.serializers import (
    TrackingRequest, TrackingResponse, TestFilters, ErrorResponse as ErrorResponseSerializer
)
from purpleserver.core.gateway import track_shipment, get_carriers
from purpleserver.proxy.router import router

logger = logging.getLogger(__name__)

DESCRIPTIONS = """
You can track a shipment by specifying the carrier and the shipment tracking number.
"""


@swagger_auto_schema(
    methods=['get'],
    tags=['Tracking'],
    responses={200: TrackingResponse(), 400: ErrorResponseSerializer()},
    operation_description=DESCRIPTIONS,
    operation_id="Retrieve",
    query_serializer=TestFilters
)
@api_view(['GET'])
@authentication_classes((SessionAuthentication, BasicAuthentication, TokenAuthentication))
@permission_classes((IsAuthenticated, ))
@throttle_classes([UserRateThrottle, AnonRateThrottle])
def track(request: Request, carrier_name: str, tracking_number: str):
    try:
        try:
            carrier_setting = next(
                iter(get_carriers(carrier_name=carrier_name, test='test' in request.query_params or None)),
                None
            )
            tracking_request = TrackingRequest(data=dict(tracking_numbers=[tracking_number]))

            if carrier_setting is None:
                raise Exception(f'No configured carrier of type: {carrier_name}')

            tracking_request.is_valid(raise_exception=True)
            response = track_shipment(tracking_request.data, carrier_setting)

            if isinstance(response, ErrorResponse):
                Response(to_dict(response), status=status.HTTP_400_BAD_REQUEST)
            return Response(
                to_dict(response),
                status=status.HTTP_200_OK if response.tracking_details is not None else status.HTTP_404_NOT_FOUND
            )

        except ValidationError as ve:
            logger.exception(ve)
            return Response(ve.args, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        logger.exception(e)
        return Response(e.args, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


router.urls.append(path('proxy/tracking/<carrier_name>/<tracking_number>', track))
