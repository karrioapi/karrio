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
    CharField, ChoiceField, COUNTRIES, ListField,

    Rate,
    Payment,
    Address as BaseAddress,
    ShipmentResponse,
    ShipmentPayload,
    ErrorResponse as ErrorResponseSerializer,
)
from purpleserver.core.gateway import Shipments
from purpleserver.proxy.router import router

logger = logging.getLogger(__name__)

DESCRIPTIONS = """
Once a Shipment is initialized by fetching the rates, the remaining requirements might be specified 
to submit the shipment to the carrier of the selected rate of your choice.
"""


class ShipmentRequest(ShipmentPayload):
    selected_rate_id = CharField(required=True, help_text="The shipment selected rate.")
    rates = ListField(child=Rate(), help_text="The list for shipment rates fetched previously")
    payment = Payment(required=True, help_text="The payment details")


class Address(BaseAddress):
    city = CharField(required=True, help_text="The address city")
    person_name = CharField(required=True, help_text="attention to")
    country_code = ChoiceField(required=True, choices=COUNTRIES, help_text="The address country code")
    address_line1 = CharField(required=True, help_text="The address line with street number")


class ShipmentRequestValidation(ShipmentRequest):
    shipper = Address(required=True, help_text="The origin address of the shipment (address from)")
    recipient = Address(required=True, help_text="The shipment destination address (address to)")


@swagger_auto_schema(
    methods=['post'],
    tags=['Shipment'],
    operation_id="proxy_create_shipment",
    operation_summary="Create a Shipment",
    operation_description=DESCRIPTIONS,
    request_body=ShipmentRequest(),
    responses={200: ShipmentResponse(), 400: ErrorResponseSerializer()},
)
@api_view(['POST'])
@authentication_classes((SessionAuthentication, BasicAuthentication, TokenAuthentication))
@permission_classes((IsAuthenticated, ))
@throttle_classes([UserRateThrottle, AnonRateThrottle])
def ship(request: Request):
    try:
        try:
            shipping_request = ShipmentRequestValidation(data=request.data)
            shipping_request.is_valid(raise_exception=True)

            response = Shipments.create(
                shipping_request.data,
                resolve_tracking_url=(
                    lambda trackin_url, shipping: reverse(
                        "purpleserver.proxy:TrackShipment",
                        request=request,
                        kwargs=dict(tracking_number=shipping.tracking_number, carrier_name=shipping.carrier_name)
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


router.urls.append(path('proxy/shipments', ship))
