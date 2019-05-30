from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes, throttle_classes
from rest_framework.response import Response
from django.urls import path

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from purplship.domain.Types import PickupRequest
from gds_helpers import to_dict


from purplship_api import serializers
from purplship_api.gateway import Gateway
from purplship_api.router import router
from purplship_api.proxies import Proxies


@swagger_auto_schema(
    methods=['post'],
    responses={201: serializers.pickup_response()},
    request_body=serializers.PickupRequest(),
    operation_id="bookPickup",
    operation_description='POST /v1/pickups',
    manual_parameter=[
        openapi.Parameter(
            'carrier', 
            openapi.IN_PATH, 
            description="specific shipping carrier", 
            type=openapi.TYPE_STRING
        )
    ]
)
@swagger_auto_schema(
    methods=['put'],
    responses={200: serializers.pickup_response()},
    request_body=serializers.PickupRequest(),
    operation_id="updatePickup",
    operation_description='PUT /v1/pickups',
    manual_parameter=[
        openapi.Parameter(
            'carrier', 
            openapi.IN_PATH, 
            description="specific shipping carrier", 
            type=openapi.TYPE_STRING
        )
    ]
)
@api_view(['POST', 'PUT'])
@authentication_classes((SessionAuthentication, BasicAuthentication, TokenAuthentication))
@permission_classes((IsAuthenticated, ))
@throttle_classes([UserRateThrottle, AnonRateThrottle])
def pickup_request(request, carrier=None):  
    """
    For creating an updating a pickup request
    * Only 'dhl' carrier is currently supported
    """
    try:
        if carrier is None or carrier not in Proxies:
            return Response("Please specify a valid carrier", status=status.HTTP_400_BAD_REQUEST)

        reqData = serializers.PickupRequest(data=request.data)
        if reqData.is_valid(raise_exception=True):
            update = request.method == 'PUT'
            operation = Gateway.modify_pickup if update else Gateway.request_pickup
            pickup, errors = operation(PickupRequest(**reqData.data), Proxies.get(carrier))
            if pickup is None and len(errors) > 0:
                rstatus = status.HTTP_400_BAD_REQUEST
            else:
                rstatus = status.HTTP_200_OK if update else status.HTTP_201_CREATED
            return Response(
                to_dict({ "pickup": pickup, "errors": errors }), 
                status=rstatus
            )
        else:
            return Response(reqData.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response(e.args, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


router.urls.append(path('pickups/<carrier>', pickup_request, name='pickups'))