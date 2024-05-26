import logging
from django.urls import path
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response

from karrio.server.core.views.api import APIView
from karrio.server.core.serializers import (
    RateRequest,
    RateResponse,
    ErrorResponse,
    ErrorMessages,
)
from karrio.server.core.gateway import Rates
from karrio.server.proxy.router import router
import karrio.server.openapi as openapi

logger = logging.getLogger(__name__)
ENDPOINT_ID = "@@"  # This endpoint id is used to make operation ids unique make sure not to duplicate

DESCRIPTIONS = """
The Shipping process begins by fetching rates for your shipment.
Use this service to fetch a shipping rates available.
"""


class RateViewAPI(APIView):
    throttle_scope = "carrier_request"

    @openapi.extend_schema(
        tags=["Proxy"],
        operation_id=f"{ENDPOINT_ID}fetch_rates",
        extensions={"x-operationId": "fetchRates"},
        summary="Fetch shipment rates",
        description=DESCRIPTIONS,
        responses={
            200: RateResponse(),
            400: ErrorResponse(),
            424: ErrorMessages(),
            500: ErrorResponse(),
        },
        request=RateRequest(),
    )
    def post(self, request: Request):
        payload = RateRequest.map(data=request.data).data

        response = Rates.fetch(payload, context=request)
        status_code = (
            status.HTTP_207_MULTI_STATUS
            if len(response.messages) > 0
            else status.HTTP_200_OK
        )

        return Response(RateResponse(response).data, status=status_code)


router.urls.append(path("proxy/rates", RateViewAPI.as_view(), name="shipment-rates"))
