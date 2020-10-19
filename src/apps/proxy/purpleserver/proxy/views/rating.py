import logging
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from django.urls import path

from drf_yasg.utils import swagger_auto_schema

from purplship.core.utils.helpers import to_dict

from purpleserver.core.views.api import GenericAPIView
from purpleserver.core.serializers import (
    RateRequest, RateResponse, ErrorResponse
)
from purpleserver.core.gateway import Rates
from purpleserver.proxy.router import router

logger = logging.getLogger(__name__)
ENDPOINT_ID = "@"  # This endpoint id is used to make operation ids unique make sure not to duplicate

DESCRIPTIONS = """
**[proxy]**

The Shipping process begins by fetching rates for your shipment.
Use this service to fetch a shipping rates available.
"""


class RateViewAPI(GenericAPIView):

    @swagger_auto_schema(
        tags=['Rates'],
        operation_id=f"{ENDPOINT_ID}fetch",
        operation_summary="Fetch shipment rates",
        operation_description=DESCRIPTIONS,
        responses={200: RateResponse(), 400: ErrorResponse()},
        request_body=RateRequest(),
    )
    def post(self, request: Request):
        rate_request = RateRequest(data=request.data)
        rate_request.is_valid(raise_exception=True)

        response = Rates.fetch(rate_request.validated_data)

        return Response(
            to_dict(response),
            status=status.HTTP_207_MULTI_STATUS if len(response.messages) > 0 else status.HTTP_201_CREATED
        )


router.urls.append(path('proxy/rates', RateViewAPI.as_view(), name="shipment-rates"))
