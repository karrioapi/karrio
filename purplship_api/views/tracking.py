from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes, throttle_classes
from rest_framework.response import Response
from django.urls import path

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from purplship.domain.Types import TrackingRequest
from gds_helpers import to_dict

from purplship_api import serializers
from purplship_api.gateway import Gateway
from purplship_api.router import router
from purplship_api.proxies import prune_carrier, filter_proxies, Proxies


class extended_tracking_request(serializers.TrackingRequest):
    carriers = serializers.StringListField(required=False, help_text="""
        Note: the 'carriers' field allows you to specify the list of carriers
        your request is targetting. 
        When no carriers are specified the request is sent to all of them

        This server is currently configured with these carriers: 'ups', 'dhl', 'fedex', 'caps', 'aups'
        Check the documentation to find carriers aliases
    """)


@swagger_auto_schema(
    method='post',
    request_body=serializers.TrackingRequest(),
    responses={200: serializers.multi_tracking_response()},
    operation_description="""
    POST /v1/tracks/[carrier]
    """,
    operation_id="getTracks",
    manual_parameter=[
        openapi.Parameter(
            'carrier', 
            openapi.IN_PATH, 
            description="specific shipping carrier", 
            type=openapi.TYPE_STRING
        )
    ]
)
@api_view(['POST'])
@authentication_classes((SessionAuthentication, BasicAuthentication, TokenAuthentication))
@permission_classes((IsAuthenticated, ))
@throttle_classes([UserRateThrottle, AnonRateThrottle])
def request(request, carrier: str = None):
    try:
        carriers = ([carrier] if carrier is not None else request.data.get('carriers')) or []
        reqData = extended_tracking_request(data=dict(list(request.data.items()) + [('carriers', carriers)]))

        if reqData.is_valid(raise_exception=True):
            data, request_proxies = prune_carrier(reqData.data)
            payload = TrackingRequest(**data)
            trackings = Gateway.get_tracking(payload, request_proxies)
            rstatus = status.HTTP_207_MULTI_STATUS if len(trackings[1]) > 0 else status.HTTP_200_OK
            response = to_dict({ "tracking": trackings[0], "errors": trackings[1] })
            return Response(response, status=rstatus)
        else:
            return Response(reqData.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response(e.args, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@swagger_auto_schema(
    methods=['get'],
    responses={200: serializers.tracking_response()},
    operation_description="""
    GET /v1/tracks/[carrier]/[tracking_number]
    """,
    operation_id="getTrack",
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
def track(request, carrier: str = None, tracking_number: str = None):
    """
    """
    error = None
    try:
        if carrier is None or carrier not in Proxies:
            error = "Please specify a valid carrier"
        if tracking_number is None:
            error = "tracking number should be specified"
        if error is None:
            payload = TrackingRequest(tracking_numbers=[tracking_number])
            trackings, errors = Gateway.get_tracking(payload, filter_proxies([carrier]))
            tracking = trackings[0] if len(trackings) > 0 else None
            return Response(
                to_dict({ "tracking": tracking, "errors": errors }), 
                status=status.HTTP_200_OK if tracking is not None else status.HTTP_404_NOT_FOUND
            )
        else:
            return Response(error, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response(e.args, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


router.urls.append(path('tracks/<carrier>', request, name='tracks'))
router.urls.append(path('tracks/<carrier>/<tracking_number>', track, name='tracks'))
