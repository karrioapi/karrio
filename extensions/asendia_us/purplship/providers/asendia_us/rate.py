from typing import Tuple, List
from asendia_us_lib.shipping_rate_request import ShippingRateRequest
from asendia_us_lib.shipping_rate_response import ShippingRate
from purplship.core.units import Packages, Services, Options
from purplship.core.utils import Serializable, DP, NF
from purplship.core.models import (
    RateRequest,
    RateDetails,
    Message
)
from purplship.providers.asendia_us.units import Service, Option, ProcessingLocation
from purplship.providers.asendia_us.error import parse_error_response
from purplship.providers.asendia_us.utils import Settings


def parse_rate_response(response: dict, settings: Settings) -> Tuple[List[RateDetails], List[Message]]:
    errors = parse_error_response(response, settings)
    details = [
        _extract_details(detail, settings)
        for detail in (response.get('shippingRates') or [])
    ]

    return details, errors


def _extract_details(detail: dict, settings: Settings) -> RateDetails:
    rate = DP.to_object(ShippingRate, detail)

    return RateDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,

        currency=rate.currencyType,
        service=Service.map(rate.productCode).name_or_key,
        base_charge=NF.decimal(rate.rate),
        total_charge=NF.decimal(rate.rate)
    )


def rate_request(payload: RateRequest, settings: Settings) -> Serializable[ShippingRateRequest]:
    package = Packages(payload.parcels).single
    service = (Services(payload.services, Service).first or Service.asendia_us_all).value
    options = Options(payload.options, Option)

    request = ShippingRateRequest(
        accountNumber=settings.account_number,
        subAccountNumber=options.asendia_sub_account_number,
        processingLocation=ProcessingLocation.map(options.asendia_processing_location or "SFO").name,
        recipientPostalCode=payload.recipient.postal_code,
        recipientCountryCode=payload.recipient.country_code,
        totalPackageWeight=package.weight.value,
        weightUnit=package.weight_unit.value.lower(),
        dimLength=package.length.value,
        dimWidth=package.width.value,
        dimHeight=package.height.value,
        dimUnit=package.dimension_unit.value,
        productCode=service,
    )

    return Serializable(request, DP.to_dict)
