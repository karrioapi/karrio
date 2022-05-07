from typing import List, Tuple

import easypost_lib.shipment_request as easypost
from easypost_lib.shipments_response import Shipment
from karrio.core.utils import Serializable, NF, DP
from karrio.core.models import RateRequest, RateDetails, Message
from karrio.core.units import Packages, Options
from karrio.providers.easypost.utils import Settings
from karrio.providers.easypost.units import (
    Service,
    PackagingType,
    Option,
)
from karrio.providers.easypost.error import parse_error_response


def parse_rate_response(
    response: dict, settings: Settings
) -> Tuple[RateDetails, List[Message]]:
    errors = [parse_error_response(response, settings)] if "error" in response else []
    rates = _extract_details(response, settings) if "error" not in response else []

    return rates, errors


def _extract_details(response: dict, settings: Settings) -> List[RateDetails]:
    rates = DP.to_object(Shipment, response).rates

    return [
        (
            lambda rate_provider, service, service_name: RateDetails(
                carrier_id=settings.carrier_id,
                carrier_name=settings.carrier_name,
                service=service,
                currency=rate.currency,
                total_charge=NF.decimal(rate.rate),
                transit_days=rate.delivery_days,
                meta=dict(
                    service_name=service_name,
                    rate_provider=rate_provider,
                ),
            )
        )(*Service.info(rate.service, rate.carrier))
        for rate in rates
    ]


def rate_request(payload: RateRequest, _) -> Serializable:
    package = Packages(payload.parcels).single
    options = Options(payload.options, Option)

    requests = easypost.ShipmentRequest(
        shipment=easypost.Shipment(
            reference=payload.reference,
            to_address=easypost.Address(
                company=payload.recipient.company_name,
                street1=payload.recipient.address_line1,
                street2=payload.recipient.address_line2,
                city=payload.recipient.city,
                state=payload.recipient.state_code,
                zip=payload.recipient.postal_code,
                country=payload.recipient.country_code,
                residential=payload.recipient.residential,
                name=payload.recipient.person_name,
                phone=payload.recipient.phone_number,
                email=payload.recipient.email,
                federal_tax_id=payload.recipient.federal_tax_id,
                state_tax_id=payload.recipient.state_tax_id,
            ),
            from_address=easypost.Address(
                company=payload.shipper.company_name,
                street1=payload.shipper.address_line1,
                street2=payload.shipper.address_line2,
                city=payload.shipper.city,
                state=payload.shipper.state_code,
                zip=payload.shipper.postal_code,
                country=payload.shipper.country_code,
                residential=payload.shipper.residential,
                name=payload.shipper.person_name,
                phone=payload.shipper.phone_number,
                email=payload.shipper.email,
                federal_tax_id=payload.shipper.federal_tax_id,
                state_tax_id=payload.shipper.state_tax_id,
            ),
            parcel=easypost.Parcel(
                length=package.length.IN,
                width=package.width.IN,
                height=package.height.IN,
                weight=package.weight.OZ,
                predefined_package=PackagingType.map(package.packaging_type).value,
            ),
            options={
                getattr(option, "key", option): getattr(option, "value", None)
                for code, option in options
                if code in Option
            },
        )
    )

    return Serializable(requests, DP.to_dict, logged=True)
