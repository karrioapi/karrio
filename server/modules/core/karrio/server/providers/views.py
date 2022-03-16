import logging

from drf_yasg import openapi
from django.urls import path
from rest_framework import status
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.request import Request
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema

from karrio.server import serializers
from karrio.server.serializers import SerializerDecorator, PaginatedResult
from karrio.server.core.views.api import GenericAPIView, APIView
from karrio.server.core.gateway import Carriers
from karrio.server.core import dataunits
from karrio.server.core.serializers import (
    CarrierSettings,
    ErrorResponse,
    FlagField,
    FlagsSerializer,
    CARRIERS,
)
from karrio.server.providers.router import router

logger = logging.getLogger(__name__)
ENDPOINT_ID = "&&"  # This endpoint id is used to make operation ids unique make sure not to duplicate
CarriersSettingsList = PaginatedResult("CarrierList", CarrierSettings)


class CarrierFilters(FlagsSerializer):

    carrier_name = serializers.ChoiceField(
        choices=CARRIERS, required=False, help_text="Indicates a carrier (type)"
    )
    test = FlagField(
        required=False,
        allow_null=True,
        default=None,
        help_text="This flag filter out carriers in test or live mode",
    )
    active = FlagField(
        required=False,
        allow_null=True,
        default=None,
        help_text="This flag indicates whether to return active carriers only",
    )
    system_only = FlagField(
        required=False,
        allow_null=True,
        default=False,
        help_text="This flag indicates that only system carriers should be returned",
    )


class CarrierList(GenericAPIView):
    pagination_class = LimitOffsetPagination
    default_limit = 100

    @swagger_auto_schema(
        tags=["Carriers"],
        operation_id=f"{ENDPOINT_ID}list",
        operation_summary="List all carriers",
        responses={200: CarriersSettingsList(), 400: ErrorResponse()},
        query_serializer=CarrierFilters,
        code_examples=[
            {
                "lang": "bash",
                "source": """
                curl --request GET \\
                  --url '/v1/carriers' \\
                  --header 'Authorization: Token <API_KEY>'
                """,
            }
        ],
    )
    def get(self, request: Request):
        """
        Returns the list of configured carriers
        """
        query = SerializerDecorator[CarrierFilters](data=request.query_params).data

        carriers = [
            carrier.data for carrier in Carriers.list(**{**query, "context": request})
        ]
        response = self.paginate_queryset(CarrierSettings(carriers, many=True).data)
        return self.get_paginated_response(response)


class CarrierServices(APIView):
    @swagger_auto_schema(
        tags=["Carriers"],
        operation_id=f"{ENDPOINT_ID}get_services",
        operation_summary="Get carrier services",
        manual_parameters=[
            openapi.Parameter(
                "carrier_name",
                openapi.IN_PATH,
                type=openapi.TYPE_STRING,
                enum=[c for c, _ in CARRIERS],
            )
        ],
        responses={
            200: openapi.Schema(type=openapi.TYPE_OBJECT, additional_properties=True)
        },
    )
    def get(self, request: Request, carrier_name: str):
        """
        Retrieve a carrier's services
        """
        references = dataunits.contextual_reference(request)

        if carrier_name not in references["carriers"]:
            raise Exception(f"Unknown carrier: {carrier_name}")

        services = references["services"].get(carrier_name, {})

        return Response(services, status=status.HTTP_200_OK)


router.urls.append(path("carriers", CarrierList.as_view()))
router.urls.append(
    path(
        "carriers/<str:carrier_name>/services",
        CarrierServices.as_view(),
        name="carrier-services",
    )
)
