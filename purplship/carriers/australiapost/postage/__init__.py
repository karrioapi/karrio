"""PurplShip Australia post postage calculation service mapper module."""

from typing import List, Union, Tuple
import pyaustraliapost.international_parcel_postage
import pyaustraliapost.domestic_letter_postage
import pyaustraliapost.international_letter_postage
import pyaustraliapost.domestic_parcel_postage
from pyaustraliapost.domestic_parcel_postage import ServiceResponse, Service
from purplship.core.utils import to_dict, Serializable, decimal
from purplship.core.units import Country, PackagingUnit, Currency
from purplship.core.models import Message, RateRequest, RateDetails
from purplship.carriers.australiapost.utils import Settings
from purplship.core.errors import OriginNotServicedError
from purplship.carriers.australiapost.postage.calculate_domestic_letter import (
    calculate_domestic_letter_request,
)
from purplship.carriers.australiapost.postage.calculate_domestic_parcel import (
    calculate_domestic_parcel_request,
)
from purplship.carriers.australiapost.postage.calculate_international_letter import (
    calculate_international_letter_request,
)
from purplship.carriers.australiapost.postage.calculate_international_parcel import (
    calculate_international_parcel_request,
)
from purplship.carriers.australiapost.error import parse_error_response

PostageRateRequest = Union[
    pyaustraliapost.international_parcel_postage.ServiceRequest,
    pyaustraliapost.domestic_letter_postage.ServiceRequest,
    pyaustraliapost.international_letter_postage.ServiceRequest,
    pyaustraliapost.domestic_parcel_postage.ServiceRequest,
]


def parse_service_response(
    response: dict, settings: Settings
) -> Tuple[List[RateDetails], List[Message]]:
    services: List[Service] = (
        ServiceResponse(**response).services.service if "services" in response else []
    )
    return (
        [_extract_quote(svc, settings) for svc in services],
        parse_error_response(response, settings),
    )


def _extract_quote(service: Service, settings: Settings) -> RateDetails:
    return RateDetails(
        carrier=settings.carrier,
        carrier_name=settings.carrier_name,
        service=service.name,
        base_charge=decimal(service.price),
        total_charge=decimal(service.price),
        currency=Currency.AUD.name,
    )


def calculate_postage_request(
    payload: RateRequest, settings: Settings
) -> Serializable[PostageRateRequest]:
    if payload.shipper.country_code and payload.shipper.country_code != Country.AU.name:
        raise OriginNotServicedError(
            payload.shipper.country_code, settings.carrier_name
        )

    is_letter: bool = (
        any(svc for svc in payload.services if "letter" in svc)
        or payload.parcel.packaging_type == PackagingUnit.envelope.name
        or payload.parcel.packaging_type == PackagingUnit.pak.name
    )
    is_international = (
        payload.recipient.country_code is None
        or payload.recipient.country_code == Country.AU.name
    )

    if is_letter and not is_international:
        request = calculate_domestic_letter_request(payload)

    elif is_letter and is_international:
        request = calculate_international_letter_request(payload)

    elif not is_letter and not is_international:
        request = calculate_domestic_parcel_request(payload)

    else:
        request = calculate_international_parcel_request(payload)

    return Serializable(request, _request_serializer)


def _request_serializer(request: PostageRateRequest) -> dict:
    return to_dict(request)
