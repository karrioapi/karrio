import logging
from django.urls import path
from rest_framework import status
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.reverse import reverse
from drf_yasg.utils import swagger_auto_schema

from purplship.core.utils.helpers import to_dict
from purpleserver.core.views.api import GenericAPIView
from purpleserver.proxy.router import router
from purpleserver.core.utils import SerializerDecorator
from purpleserver.core.gateway import Shipments
from purpleserver.core.serializers import (
    CharField, ChoiceField, COUNTRIES,

    ShippingRequest,
    ShipmentCancelRequest,
    OperationResponse,
    Address as BaseAddress,
    ShipmentResponse,
    ErrorResponse,
    TestFilters,
)

logger = logging.getLogger(__name__)
ENDPOINT_ID = "@@"  # This endpoint id is used to make operation ids unique make sure not to duplicate

DESCRIPTIONS = """
**[proxy]**

Once the shipping rates are retrieved, provide the required info to
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


class ShippingList(GenericAPIView):

    @swagger_auto_schema(
        tags=['Shipping'],
        operation_id=f"{ENDPOINT_ID}buy_label",
        operation_summary="Buy a shipment label",
        operation_description=DESCRIPTIONS,
        request_body=ShippingRequest(),
        responses={200: ShipmentResponse(), 400: ErrorResponse()},
    )
    def post(self, request: Request):
        payload = SerializerDecorator[ShippingRequestValidation](data=request.data).data

        response = Shipments.create(
            payload,
            resolve_tracking_url=(
                lambda shipment: reverse(
                    "purpleserver.proxy:shipment-tracking",
                    kwargs=dict(tracking_number=shipment.tracking_number, carrier_name=shipment.carrier_name)
                )
            )
        )

        return Response(to_dict(response), status=status.HTTP_201_CREATED)


class ShippingDetails(GenericAPIView):

    @swagger_auto_schema(
        tags=['Shipping'],
        operation_id=f"{ENDPOINT_ID}void_label",
        operation_summary="Void a shipment label",
        operation_description="**[proxy]**\n\nCancel a shipment and the label previously created",
        request_body=ShipmentCancelRequest(),
        responses={200: OperationResponse(), 400: ErrorResponse()},
    )
    def post(self, request: Request, carrier_name: str):
        filters = SerializerDecorator[TestFilters](data=request.query_params).data
        payload = SerializerDecorator[ShipmentCancelRequest](data=request.data).data

        response = Shipments.track(payload, carrier_filter={**filters, 'carrier_name': carrier_name})

        return Response(to_dict(response), status=status.HTTP_202_ACCEPTED)


router.urls.append(path('proxy/shipping', ShippingList.as_view(), name="shipping-request"))
router.urls.append(path('proxy/shipping/<carrier_name>/cancel', ShippingDetails.as_view(), name="shipping-cancel"))
