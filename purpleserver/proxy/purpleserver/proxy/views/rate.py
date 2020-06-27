import logging
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes, throttle_classes
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from django.urls import path

from drf_yasg.utils import swagger_auto_schema

from purplship.core.utils.helpers import to_dict

from purpleserver.core.serializers import (
    RateRequest, RateResponse, ErrorResponse as ErrorResponseSerializer
)
from purpleserver.core.gateway import Carriers, Rates
from purpleserver.proxy.router import router

logger = logging.getLogger(__name__)

DESCRIPTIONS = """
The Shipping process begins by fetching rates for your shipment.
The request returns rates required to create your shipment.
"""


@swagger_auto_schema(
    methods=['post'],
    tags=['Rate'],
    operation_id="proxy_fetch_rates",
    operation_summary="Fetch Shipment Rates",
    operation_description=DESCRIPTIONS,
    responses={200: RateResponse(), 400: ErrorResponseSerializer()},
    request_body=RateRequest(),
)
@api_view(['POST'])
@authentication_classes((SessionAuthentication, BasicAuthentication, TokenAuthentication))
@permission_classes((IsAuthenticated, ))
@throttle_classes([UserRateThrottle, AnonRateThrottle])
def fetch_rates(request: Request):
    rate_request = RateRequest(data=request.data)
    rate_request.is_valid(raise_exception=True)

    carrier_settings_list = Carriers.list(
        carrier_ids=rate_request.data.get('carrier_ids', [])
    )

    if len(carrier_settings_list) == 0:
        raise NotFound("No configured carriers specified")

    response = Rates.fetch(rate_request.data, carrier_settings_list)

    return Response(
        to_dict(response),
        status=status.HTTP_207_MULTI_STATUS if len(response.messages) > 0 else status.HTTP_201_CREATED
    )


router.urls.append(path('proxy/rates', fetch_rates))
