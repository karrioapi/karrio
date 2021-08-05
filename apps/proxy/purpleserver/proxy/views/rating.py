import logging
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from django.urls import path

from purpleserver.serializers import SerializerDecorator
from purpleserver.core.views.api import APIView
from purpleserver.core.serializers import (
    RateRequest, RateResponse, ErrorResponse, TestFilters
)
from purpleserver.core.gateway import Rates
from purpleserver.proxy.router import router

logger = logging.getLogger(__name__)
ENDPOINT_ID = "@@"  # This endpoint id is used to make operation ids unique make sure not to duplicate

DESCRIPTIONS = """
The Shipping process begins by fetching rates for your shipment.
Use this service to fetch a shipping rates available.
"""


class RateViewAPI(APIView):

    @swagger_auto_schema(
        tags=['Proxy'],
        operation_id=f"{ENDPOINT_ID}fetch_rates",
        operation_summary="Fetch shipment rates",
        operation_description=DESCRIPTIONS,
        responses={200: RateResponse(), 400: ErrorResponse()},
        request_body=RateRequest(),
        query_serializer=TestFilters(),
    )
    def post(self, request: Request):
        payload = SerializerDecorator[RateRequest](data=request.data).data
        test_filter = SerializerDecorator[TestFilters](data=request.query_params).data

        response = Rates.fetch(payload, context=request, **test_filter)

        return Response(
            RateResponse(response).data,
            status=status.HTTP_207_MULTI_STATUS if len(response.messages) > 0 else status.HTTP_201_CREATED
        )


router.urls.append(path('proxy/rates', RateViewAPI.as_view(), name="shipment-rates"))
