import logging
from django.urls import path
from rest_framework import status
from rest_framework.response import Response
from rest_framework.request import Request

import karrio.server.openapi as openapi
import karrio.server.core.dataunits as dataunits
from karrio.server.core.views.api import APIView
from karrio.server.core.serializers import (
    TrackingResponse,
    ErrorResponse,
    ErrorMessages,
)
from karrio.server.core.gateway import Shipments
from karrio.server.proxy.router import router

logger = logging.getLogger(__name__)
ENDPOINT_ID = "@@@@"  # This endpoint id is used to make operation ids unique make sure not to duplicate


class TrackingAPIView(APIView):
    logging_methods = ["GET"]

    @openapi.extend_schema(
        tags=["Proxy"],
        operation_id=f"{ENDPOINT_ID}track_shipment",
        summary="Track a shipment",
        responses={
            200: TrackingResponse(),
            400: ErrorResponse(),
            424: ErrorMessages(),
            500: ErrorResponse(),
        },
        parameters=[
            openapi.OpenApiParameter(
                "carrier_name",
                location=openapi.OpenApiParameter.PATH,
                type=openapi.OpenApiTypes.STR,
                enum=dataunits.NON_HUBS_CARRIERS,
                required=True,
            ),
            openapi.OpenApiParameter(
                "tracking_number",
                location=openapi.OpenApiParameter.PATH,
                type=openapi.OpenApiTypes.STR,
                required=True,
            ),
            openapi.OpenApiParameter(
                "hub",
                location=openapi.OpenApiParameter.QUERY,
                type=openapi.OpenApiTypes.STR,
                required=False,
            ),
        ],
    )
    def get(self, request: Request, carrier_name: str, tracking_number: str):
        """
        You can track a shipment by specifying the carrier and the shipment tracking number.
        """
        query = request.query_params
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
