import logging
from typing import List
from functools import reduce
from rest_framework.authentication import BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from rest_framework_tracking.mixins import LoggingMixin
from rest_framework import status, viewsets, mixins
from rest_framework.response import Response

from drf_yasg.utils import swagger_auto_schema

from purplship.domain.Types import RateRequest, QuoteDetails, ChargeDetails
from purplship.domain.Types.units import CountryCurrency
from gds_helpers import to_dict

from purplship_api import serializers
from purplship_api.gateway import Gateway
from purplship_api.router import router
from purplship_api.proxies import prune_carrier
from purplship_api.currency import Currency

logger = logging.getLogger(__name__)


class Rates(LoggingMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    """Request quotes (rating) from carriers."""

    authentication_classes = (BasicAuthentication, TokenAuthentication)
    throttle_classes = (UserRateThrottle, AnonRateThrottle)
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.RateRequest

    @swagger_auto_schema(
        responses={200: serializers.rate_response()},
        operation_id="requestRates",
        operation_description='POST /v1/rates',
    )
    def create(self, request):
        try:
            reqData = serializers.RateRequest(data=request.data)
            if reqData.is_valid(raise_exception=True):
                data, proxies = prune_carrier(reqData.data)
                payload = RateRequest(**data)
                rates, errors = Gateway.get_quotes(payload, proxies)
                sanitized_rates = sanitize_currency(rates, payload)
                return Response(
                    to_dict({**data, "rates": sanitized_rates, "errors": errors}),
                    status=status.HTTP_207_MULTI_STATUS if len(errors) > 0 else status.HTTP_200_OK
                )
            else:
                return Response(reqData.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(e.args, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


router.register(r'rates', Rates, base_name='rates')


def sanitize_currency(rates: List[QuoteDetails], payload: RateRequest):
    try:
        if not payload.shipment.currency and not payload.shipper.country_code:
            return rates
        expected_currency = payload.shipment.currency or CountryCurrency[
            payload.shipper.country_code
        ].value
        return reduce(lambda l, r: l + [_ensure_converted(r, expected_currency)], rates, [])
    except Exception as e:
        print(f"Error during rates {rates} currency sanitize {e}")
        return rates


def _ensure_converted(rate: QuoteDetails, expected_currency: str):
    if rate.currency == expected_currency:
        return rate
    return QuoteDetails(**{
        **to_dict(rate),
        **dict(
            currency=expected_currency,
            base_charge=Currency.convert(rate.base_charge, rate.currency, expected_currency),
            duties_and_taxes=Currency.convert(rate.duties_and_taxes, rate.currency, expected_currency),
            total_charge=Currency.convert(rate.total_charge, rate.currency, expected_currency),
            discount=Currency.convert(rate.discount, rate.currency, expected_currency),
            extra_charges=[
                ChargeDetails(**{
                    **to_dict(charge),
                    **dict(
                        currency=expected_currency,
                        amount=Currency.convert(charge.amount, charge.currency, expected_currency)
                    )
                })
                for charge in rate.extra_charges
            ]
        )
    })
