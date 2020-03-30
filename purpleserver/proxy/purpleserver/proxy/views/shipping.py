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

from purplship.core.utils.helpers import to_dict

from purpleserver.core.serializers import ShipmentResponse, ShipmentRequest
from purpleserver.core.gateway import create_shipment, get_carriers
from purpleserver.proxy.router import router

logger = logging.getLogger(__name__)


@swagger_auto_schema(
    methods=['post'],
    request_body=ShipmentRequest(),
    responses={200: ShipmentResponse()},
    operation_description="""
    POST /v1/shipping
    """,
    operation_id="CreateShipment",
)
@api_view(['POST'])
@authentication_classes((SessionAuthentication, BasicAuthentication, TokenAuthentication))
@permission_classes((IsAuthenticated, ))
@throttle_classes([UserRateThrottle, AnonRateThrottle])
def ship(request: Request):
    try:
        try:
            request = ShipmentRequest(data=request.data)

            request.is_valid(raise_exception=True)
            response = create_shipment(request.data)

            return Response(to_dict(response), status=status.HTTP_201_CREATED)
        except Exception as pe:
            logger.exception(pe)
            return Response(pe.args, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        logger.exception(e)
        return Response(e.args, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


router.urls.append(path('shipping', ship, name='Shipping'))
