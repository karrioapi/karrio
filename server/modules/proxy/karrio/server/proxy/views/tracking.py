import logging
from django.urls import path
from rest_framework import status
from rest_framework.response import Response
from rest_framework.request import Request
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from karrio.server.serializers import SerializerDecorator, CharField, Serializer
from karrio.server.core.views.api import APIView
import karrio.server.core.dataunits as dataunits
from karrio.server.core.serializers import (
    TrackingResponse,
    ErrorResponse,
    ErrorMessages,
)
from karrio.server.core.gateway import Shipments
from karrio.server.proxy.router import router

logger = logging.getLogger(__name__)
ENDPOINT_ID = "@@@@"  # This endpoint id is used to make operation ids unique make sure not to duplicate


class TrackerFilter(Serializer):
    hub = CharField(
        required=False,
        allow_blank=False,
        allow_null=False,
        max_length=50,
        help_text="A carrier_name of a hub connector",
    )


class TrackingAPIView(APIView):
    logging_methods = ["GET"]

    @swagger_auto_schema(
        tags=["Proxy"],
        operation_id=f"{ENDPOINT_ID}track_shipment",
        operation_summary="Track a shipment",
        query_serializer=TrackerFilter(),
        responses={
            200: TrackingResponse(),
            400: ErrorResponse(),
            424: ErrorMessages(),
            500: ErrorResponse(),
        },
        manual_parameters=[
            openapi.Parameter(
                "carrier_name",
                in_=openapi.IN_PATH,
                type=openapi.TYPE_STRING,
                enum=dataunits.NON_HUBS_CARRIERS,
            ),
        ],
    )
    def get(self, request: Request, carrier_name: str, tracking_number: str):
        """
        You can track a shipment by specifying the carrier and the shipment tracking number.
        """
        query = SerializerDecorator[TrackerFilter](data=request.query_params).data
        carrier_filter = {
            **{k: v for k, v in query.items() if k != "hub"},
            # If a hub is specified, use the hub as carrier to track the package
            "carrier_name": (query.get("hub") if "hub" in query else carrier_name),
        }
        data = {
            "tracking_numbers": [tracking_number],
            "options": (
                {tracking_number: {"carrier": carrier_name}} if "hub" in query else {}
            ),
        }

        response = Shipments.track(data, context=request, **carrier_filter)

        return Response(
            TrackingResponse(response).data,
            status=(status.HTTP_200_OK if response.tracking is not None else status.HTTP_404_NOT_FOUND),
        )


router.urls.append(
    path(
        "proxy/tracking/<carrier_name>/<tracking_number>",
        TrackingAPIView.as_view(),
        name="shipment-tracking",
    )
)
