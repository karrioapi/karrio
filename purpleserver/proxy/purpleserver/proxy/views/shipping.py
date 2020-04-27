import logging
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes, throttle_classes
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.reverse import reverse
from django.urls import path

from drf_yasg.utils import swagger_auto_schema

from purplship.core.utils.helpers import to_dict

from purpleserver.core.datatypes import ErrorResponse
from purpleserver.core.exceptions import ValidationError
from purpleserver.core.serializers import (
    ShipmentResponse, ShipmentRequest, ShipmentOption, ErrorResponse as ErrorResponseSerializer
)
from purpleserver.core.gateway import create_shipment
from purpleserver.proxy.router import router

logger = logging.getLogger(__name__)

DESCRIPTIONS = """
Once a Shipment is initialized by fetching the rates, the remaining requirements might be specified 
to submit the shipment to the carrier of the selected rate of your choice.
"""


class ShipmentRequestSchema(ShipmentRequest):
    options = ShipmentOption(required=False, help_text=f"""
    The options available for the shipment.

    Note that this is a dictionary in which you can can add as many carrier shipment
    options you desire to add to your shipment. 

    Please consult the reference for additional specific carriers options.
    """)


@swagger_auto_schema(
    methods=['post'],
    tags=['PROXY'],
    request_body=ShipmentRequestSchema(),
    responses={200: ShipmentResponse(), 400: ErrorResponseSerializer()},
    operation_description=DESCRIPTIONS,
    operation_id="Create A Shipment",
)
@api_view(['POST'])
@authentication_classes((SessionAuthentication, BasicAuthentication, TokenAuthentication))
@permission_classes((IsAuthenticated, ))
@throttle_classes([UserRateThrottle, AnonRateThrottle])
def ship(request: Request):
    try:
        try:
            shipping_request = ShipmentRequest(data=request.data)
            shipping_request.is_valid(raise_exception=True)

            response = create_shipment(
                shipping_request.data,
                resolve_tracking_url=(
                    lambda trackin_url, shipping: reverse(
                        "Tracking",
                        request=request,
                        kwargs=dict(tracking_number=shipping.tracking_number, carrier=shipping.carrier)
                    )
                )
            )

            if isinstance(response, ErrorResponse):
                Response(to_dict(response), status=status.HTTP_400_BAD_REQUEST)
            return Response(to_dict(response), status=status.HTTP_201_CREATED)

        except ValidationError as ve:
            logger.exception(ve)
            return Response(ve.args, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        logger.exception(e)
        return Response(e.args, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


router.urls.append(path('proxy/shipments', ship, name='Shipping'))
