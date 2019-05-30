from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes, throttle_classes
from rest_framework.response import Response
from django.urls import path

from drf_yasg.utils import swagger_auto_schema

from purplship.domain.Types import ShipmentRequest
from gds_helpers import to_dict

from purplship_api import serializers
from purplship_api.gateway import Gateway
from purplship_api.router import router
from purplship_api.proxies import Proxies


@swagger_auto_schema(
    methods=['post'],
    responses={201: serializers.shipping_response()},
    request_body=serializers.ShipmentRequest(),
    operation_id="createShipment",
    operation_description='POST /v1/shipments/[carrier]',
)
@api_view(['POST'])
@authentication_classes((SessionAuthentication, BasicAuthentication, TokenAuthentication))
@permission_classes((IsAuthenticated, ))
@throttle_classes([UserRateThrottle, AnonRateThrottle])
def create(request, carrier=None):  
    """
    For creating shipment and obtain label
    * Only 'dhl' carrier is currently supported
    """
    try:
        if carrier is None or carrier not in Proxies:
            return Response("Please specify a valid carrier", status=status.HTTP_400_BAD_REQUEST)

        reqData = serializers.ShipmentRequest(data=request.data)
        if reqData.is_valid(raise_exception=True):
            shipment, errors = Gateway.create_shipment(
                ShipmentRequest(**reqData.data), 
                Proxies.get(carrier)
            )
            response = to_dict({ "shipment": shipment, "errors": errors })
            return Response(response, status=status.HTTP_201_CREATED)
        else:
            return Response(reqData.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response(e.args, status=status.HTTP_500_INTERNAL_SERVER_ERROR)





router.urls.append(path('shipments/<carrier>', create, name='shipments'))