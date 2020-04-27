import logging
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes, throttle_classes
from rest_framework.request import Request
from rest_framework.response import Response
from django.urls import path

from drf_yasg.utils import swagger_auto_schema

from purplship.core.utils.helpers import to_dict

from purpleserver.core.datatypes import ErrorResponse
from purpleserver.core.exceptions import ValidationError
from purpleserver.core.serializers import (
    RateRequest, RateResponse, CarrierFilters, ShipmentOption, ErrorResponse as ErrorResponseSerializer
)
from purpleserver.core.gateway import fetch_rates, get_carriers
from purpleserver.proxy.router import router

logger = logging.getLogger(__name__)

DESCRIPTIONS = """
The Shipping process begins by fetching rates for your shipment.
The rate request return the backbone of your shipment object adding
the rates retrieved from one or many carriers based on your filter.
"""


class RateRequestSchema(RateRequest):
    options = ShipmentOption(required=False, help_text=f"""
    The options available for the shipment.

    Note that this is a dictionary in which you can can add as many carrier shipment
    options you desire to add to your shipment. 

    Please consult the reference for additional specific carriers options.
    """)


@swagger_auto_schema(
    methods=['post'],
    tags=['PROXY'],
    responses={200: RateResponse(), 400: ErrorResponseSerializer()},
    request_body=RateRequestSchema(),
    operation_description=DESCRIPTIONS,
    operation_id="Fetch Rates",
    query_serializer=CarrierFilters
)
@api_view(['POST'])
@authentication_classes((SessionAuthentication, BasicAuthentication, TokenAuthentication))
@permission_classes((IsAuthenticated, ))
@throttle_classes([UserRateThrottle, AnonRateThrottle])
def rates(request: Request):
    try:
        try:
            query = request.query_params
            carrier_settings_list = get_carriers(
                carrier_type=query.get('carrier'),
                carrier_name=query.get('carrierName'),
            )
            rate_request = RateRequest(data=request.data)

            if len(carrier_settings_list) == 0:
                raise Exception(f'No configured carriers specified')

            rate_request.is_valid(raise_exception=True)
            response = fetch_rates(rate_request.data, carrier_settings_list)

            if isinstance(response, ErrorResponse):
                Response(to_dict(response), status=status.HTTP_400_BAD_REQUEST)
            return Response(
                to_dict(response),
                status=status.HTTP_207_MULTI_STATUS if len(response.messages) > 0 else status.HTTP_201_CREATED
            )

        except ValidationError as ve:
            logger.exception(ve)
            return Response(ve.args, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        logger.exception(e)
        return Response(e.args, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


router.urls.append(path('proxy/rates', rates, name='Rates'))
