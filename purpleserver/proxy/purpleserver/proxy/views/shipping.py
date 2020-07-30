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

from purpleserver.proxy.router import router
from purpleserver.core.gateway import Shipments
from purpleserver.core.serializers import (
    CharField, ChoiceField, COUNTRIES,

    ShippingRequest,
    Address as BaseAddress,
    ShipmentResponse,
    ErrorResponse,
)

logger = logging.getLogger(__name__)

DESCRIPTIONS = """
Once the shipment rates are retrieved, provide the required info to
submit the shipment by specifying your preferred rate.
"""


class Address(BaseAddress):
    city = CharField(required=True, help_text="The address city")
    person_name = CharField(required=True, help_text="attention to")
    country_code = ChoiceField(required=True, choices=COUNTRIES, help_text="The address country code")
    address_line1 = CharField(required=True, help_text="The address line with street number")


class ShippingRequestValidation(ShippingRequest):
    shipper = Address(required=True, help_text="The origin address of the shipment (address from)")
    recipient = Address(required=True, help_text="The shipment destination address (address to)")


@swagger_auto_schema(
    methods=['post'],
    tags=['Shipping'],
    operation_id="proxy_create_shipping",
    operation_summary="Submit a Shipment",
    operation_description=DESCRIPTIONS,
    request_body=ShippingRequest(),
    responses={200: ShipmentResponse(), 400: ErrorResponse()},
)
@api_view(['POST'])
@authentication_classes((SessionAuthentication, BasicAuthentication, TokenAuthentication))
@permission_classes((IsAuthenticated, ))
@throttle_classes([UserRateThrottle, AnonRateThrottle])
def submit_shipment(request: Request):
    shipping_request = ShippingRequestValidation(data=request.data)
    shipping_request.is_valid(raise_exception=True)

    response = Shipments.create(
        shipping_request.data,
        resolve_tracking_url=(
            lambda shipment: reverse(
                "purpleserver.proxy:shipment-tracking",
                request=request,
                kwargs=dict(tracking_number=shipment.tracking_number, carrier_name=shipment.carrier_name)
            )
        )
    )

    return Response(to_dict(response), status=status.HTTP_201_CREATED)


router.urls.append(path('proxy/shipping', submit_shipment, name="shipping-request"))
