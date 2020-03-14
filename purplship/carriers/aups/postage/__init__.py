"""PurplShip Australia post postage calculation service mapper module."""

from typing import List, Union, Tuple
import pyaups.international_parcel_postage
import pyaups.domestic_letter_postage
import pyaups.international_letter_postage
import pyaups.domestic_parcel_postage
from pyaups.domestic_parcel_postage import ServiceResponse, Service
from purplship.core.utils.helpers import to_dict
from purplship.core.utils.serializable import Serializable
from purplship.core.units import Country, PackagingUnit, Currency
from purplship.core.models import Error, RateRequest, RateDetails
from purplship.carriers.aups.utils import Settings
from purplship.core.errors import OriginNotServicedError
from purplship.carriers.aups.postage.calculate_domestic_letter import (
    calculate_domestic_letter_request,
)
from purplship.carriers.aups.postage.calculate_domestic_parcel import (
    calculate_domestic_parcel_request,
)
from purplship.carriers.aups.postage.calculate_international_letter import (
    calculate_international_letter_request,
)
from purplship.carriers.aups.postage.calculate_international_parcel import (
    calculate_international_parcel_request,
)

PostageRateRequest = Union[
    pyaups.international_parcel_postage.ServiceRequest,
    pyaups.domestic_letter_postage.ServiceRequest,
    pyaups.international_letter_postage.ServiceRequest,
    pyaups.domestic_parcel_postage.ServiceRequest,
]


def parse_service_response(
    self, response: dict
) -> Tuple[List[RateDetails], List[Error]]:
    services: List[Service] = (
        ServiceResponse(**response).services.service if "services" in response else []
    )
    return (
        [self._extract_quote(svc) for svc in services],
        self.parse_error_response(response),
    )


def _extract_quote(self, service: Service) -> RateDetails:
    return RateDetails(
        carrier=self.client.carrier_name,
        service_name=service.name,
        service_type=service.code,
        base_charge=float(service.price),
        duties_and_taxes=0,
        total_charge=float(service.price),
        currency=Currency.AUD.name,
        delivery_date=None,
        discount=0,
        extra_charges=None,
    )


def calculate_postage_request(
    payload: RateRequest, settings: Settings
) -> Serializable[PostageRateRequest]:
    if payload.shipper.country_code and payload.shipper.country_code != Country.AU.name:
        raise OriginNotServicedError(
            payload.shipper.country_code, settings.carrier_name
        )

    is_letter: bool = (
        any(svc for svc in payload.parcel.services if "LETTER" in svc)
        or payload.parcel.packaging_type == PackagingUnit.SM.name
        or payload.parcel.packaging_type == PackagingUnit.SM.name
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
