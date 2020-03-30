import logging
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes, throttle_classes
from rest_framework.response import Response
from django.urls import path

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from purplship.core.utils import to_dict
from purpleserver.core.serializers import TrackingRequest, CompleteTrackingResponse
from purpleserver.core.gateway import track_shipment, get_carriers
from purpleserver.proxy.router import router

logger = logging.getLogger(__name__)


@swagger_auto_schema(
    methods=['get'],
    responses={200: CompleteTrackingResponse()},
    operation_description="""
    GET /v1/tracking/[carrier]/[tracking_number]
    """,
    operation_id="TrackShipment",
    manual_parameter=[
        openapi.Parameter(
            'carrier',
            openapi.IN_PATH,
            required=True,
            description="specific shipping carrier",
            type=openapi.TYPE_STRING
        ),
        openapi.Parameter(
            'tracking_number',
            openapi.IN_PATH,
            required=True,
            description="shipment tracking number",
            type=openapi.TYPE_STRING
        )
    ]
)
@api_view(['GET'])
@authentication_classes((SessionAuthentication, BasicAuthentication, TokenAuthentication))
@permission_classes((IsAuthenticated, ))
@throttle_classes([UserRateThrottle, AnonRateThrottle])
def track(_, carrier: str, tracking_number: str):
    try:
        try:
            carrier_setting = next(iter(get_carriers(carrier_type=carrier)), None)
            request = TrackingRequest(data=dict(tracking_numbers=[tracking_number]))

            if carrier_setting is None:
                raise Exception(f'No configured carrier of type: {carrier}')

            request.is_valid(raise_exception=True)
            response = track_shipment(request.data, carrier_setting)
            print(response)
            return Response(
                to_dict(response),
                status=status.HTTP_200_OK if response.tracking_details is not None else status.HTTP_404_NOT_FOUND
            )
        except Exception as pe:
            logger.exception(pe)
            return Response(pe.args, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        logger.exception(e)
        return Response(e.args, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


router.urls.append(path('tracking/<carrier>/<tracking_number>', track, name='Tracking'))
