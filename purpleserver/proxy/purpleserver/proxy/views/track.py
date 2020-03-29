from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes, throttle_classes
from rest_framework.response import Response
from django.urls import path

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from purplship.core.utils.helpers import to_dict

from purpleserver.core import serializers
from purpleserver.core.gateway import track_shipment
from purpleserver.proxy.router import router


@swagger_auto_schema(
    methods=['get'],
    responses={200: serializers.CompleteTrackingResponse()},
    operation_description="""
    GET /v1/tracks/[carrier]/[tracking_number]
    """,
    operation_id="TrackShipment",
    manual_parameter=[
        openapi.Parameter(
            'carrier',
            openapi.IN_PATH,
            description="specific shipping carrier",
            type=openapi.TYPE_STRING
        ),
        openapi.Parameter(
            'tracking_number',
            openapi.IN_PATH,
            description="shipment tracking number",
            type=openapi.TYPE_STRING
        )
    ]
)
@api_view(['GET'])
@authentication_classes((SessionAuthentication, BasicAuthentication, TokenAuthentication))
@permission_classes((IsAuthenticated, ))
@throttle_classes([UserRateThrottle, AnonRateThrottle])
def tracking(carrier: str = None, tracking_number: str = None):
    error = None
    try:
        if error is None:
            return Response(
                to_dict({}),
                status=status.HTTP_200_OK
            )
        else:
            return Response(error, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response(e.args, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


router.urls.append(path('track/<carrier>/<tracking_number>', tracking, name='Tracking'))
