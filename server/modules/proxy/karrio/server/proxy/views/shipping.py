import logging
from django.urls import path
from rest_framework import status
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.reverse import reverse
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from karrio.server.core.views.api import APIView
from karrio.server.proxy.router import router
from karrio.server.serializers import SerializerDecorator
from karrio.server.core.gateway import Shipments
from karrio.server.core.serializers import (
    CharField,
    ChoiceField,
    COUNTRIES,
    MODELS,
    EntitySerializer,
    ShippingRequest,
    ShipmentCancelRequest,
    ShipmentContent,
    ShipmentDetails,
    OperationResponse,
    Address as BaseAddress,
    ErrorResponse,
    TestFilters,
)

logger = logging.getLogger(__name__)
ENDPOINT_ID = "@@@"  # This endpoint id is used to make operation ids unique make sure not to duplicate
CARRIER_NAMES = list(MODELS.keys())


class Address(BaseAddress):
    city = CharField(required=True, help_text="The address city")
    person_name = CharField(required=True, help_text="attention to")
    country_code = ChoiceField(
        required=True, choices=COUNTRIES, help_text="The address country code"
    )
    address_line1 = CharField(
        required=True, help_text="The address line with street number"
    )


class ShippingRequestValidation(ShippingRequest):
    shipper = Address(
        required=True, help_text="The origin address of the shipment (address from)"
    )
    recipient = Address(
        required=True, help_text="The shipment destination address (address to)"
    )


class ShippingResponse(EntitySerializer, ShipmentContent, ShipmentDetails):
    object_type = CharField(default="shipment", help_text="Specifies the object type")


class ShippingDetails(APIView):
    @swagger_auto_schema(
        tags=["Proxy"],
        operation_id=f"{ENDPOINT_ID}buy_label",
        operation_summary="Buy a shipment label",
        request_body=ShippingRequest(),
        responses={200: ShippingResponse(), 400: ErrorResponse()},
    )
    def post(self, request: Request):
        """
        Once the shipping rates are retrieved, provide the required info to
        submit the shipment by specifying your preferred rate.
        """
        payload = SerializerDecorator[ShippingRequestValidation](data=request.data).data

        response = Shipments.create(
            payload,
            resolve_tracking_url=(
                lambda tracking_number, carrier_name: reverse(
                    "karrio.server.proxy:shipment-tracking",
                    kwargs=dict(
                        tracking_number=tracking_number, carrier_name=carrier_name
                    ),
                )
            ),
        )

        return Response(ShippingResponse(response).data, status=status.HTTP_201_CREATED)


class ShippingCancel(APIView):
    @swagger_auto_schema(
        tags=["Proxy"],
        operation_id=f"{ENDPOINT_ID}void_label",
        operation_summary="Void a shipment label",
        query_serializer=TestFilters(),
        request_body=ShipmentCancelRequest(),
        responses={200: OperationResponse(), 400: ErrorResponse()},
        manual_parameters=[
            openapi.Parameter(
                "carrier_name",
                in_=openapi.IN_PATH,
                type=openapi.TYPE_STRING,
                enum=CARRIER_NAMES,
            ),
        ],
    )
    def post(self, request: Request, carrier_name: str):
        """
        Cancel a shipment and the label previously created
        """
        test_filter = SerializerDecorator[TestFilters](data=request.query_params).data
        payload = SerializerDecorator[ShipmentCancelRequest](data=request.data).data

        response = Shipments.cancel(
            payload, context=request, carrier_name=carrier_name, **test_filter
        )

        return Response(
            OperationResponse(response).data, status=status.HTTP_202_ACCEPTED
        )


router.urls.append(
    path("proxy/shipping", ShippingDetails.as_view(), name="shipping-request")
)
router.urls.append(
    path(
        "proxy/shipping/<carrier_name>/cancel",
        ShippingCancel.as_view(),
        name="shipping-cancel",
    )
)
