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
from drf_yasg import openapi

from purplship.core.utils.helpers import to_dict

from purpleserver.core.serializers import RateRequest, RateResponse
from purpleserver.core.gateway import fetch_rates, get_carriers
from purpleserver.proxy.router import router

logger = logging.getLogger(__name__)


@swagger_auto_schema(
    methods=['post'],
    responses={200: RateResponse()},
    request_body=RateRequest(),
    operation_description=(
        'POST /v1/rating?carrier=[carrier]&carrier_name=[carrier_name]'
    ),
    operation_id="ShippingRates",
    manual_parameter=[
        openapi.Parameter(
            'carrier',
            openapi.IN_QUERY,
            description="specific shipping carrier type",
            type=openapi.TYPE_STRING
        ),
        openapi.Parameter(
            'carrier_name',
            openapi.IN_QUERY,
            description="shipment name",
            type=openapi.TYPE_STRING
        )
    ]
)
@api_view(['POST'])
@authentication_classes((SessionAuthentication, BasicAuthentication, TokenAuthentication))
@permission_classes((IsAuthenticated, ))
@throttle_classes([UserRateThrottle, AnonRateThrottle])
def rate(request: Request):
    try:
        try:
            query = request.query_params
            carrier_settings_list = get_carriers(
                carrier_type=query.get('carrier'),
                carrier_name=query.get('carrier_name'),
            )
            rate_request = RateRequest(data=request.data)

            if len(carrier_settings_list) == 0:
                raise Exception(f'No configured carriers specified')

            rate_request.is_valid(raise_exception=True)
            response = fetch_rates(rate_request.data, carrier_settings_list)

            return Response(
                to_dict(response),
                status=status.HTTP_207_MULTI_STATUS if len(response.messages) > 0 else status.HTTP_200_OK
            )
        except Exception as pe:
            logger.exception(pe)
            return Response(pe.args, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        logger.exception(e)
        return Response(e.args, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


router.urls.append(path('rating', rate, name='Rates'))
