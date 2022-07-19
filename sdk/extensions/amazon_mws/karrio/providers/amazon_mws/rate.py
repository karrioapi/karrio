from typing import List, Tuple
import amazon_mws_lib.rate_request as amazon
from amazon_mws_lib.rate_response import ServiceRate
from karrio.core.utils import Serializable, SF, NF, DP, DF
from karrio.core.models import RateRequest, RateDetails, Message, ChargeDetails
from karrio.core.units import Packages, Options, Services
from karrio.providers.amazon_mws.utils import Settings
from karrio.providers.amazon_mws.units import (
    Service,
)
from karrio.providers.amazon_mws.error import parse_error_response


def parse_rate_response(
    response: dict, settings: Settings
) -> Tuple[List[RateDetails], List[Message]]:
    errors: List[Message] = sum(
        [parse_error_response(data, settings) for data in response.get("errors", [])],
        [],
    )
    rates = [
        _extract_details(data, settings) for data in response.get("serviceRates", [])
    ]

    return rates, errors


def _extract_details(data: dict, settings: Settings) -> RateDetails:
    rate = DP.to_object(ServiceRate, data)
    transit = (
        DF.date(rate.promise.deliveryWindow.start, "%Y-%m-%dT%H:%M:%S.%fZ").date()
        - DF.date(rate.promise.receiveWindow.end, "%Y-%m-%dT%H:%M:%S.%fZ").date()
    ).days

    return RateDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        service=Service.map(rate.serviceType).name_or_key,
        total_charge=NF.decimal(rate.totalCharge.value),
        currency=rate.totalCharge.unit,
        transit_days=transit,
        meta=dict(
            service_name=rate.serviceType,
        ),
    )


def rate_request(payload: RateRequest, _) -> Serializable:
    packages = Packages(payload.parcels)
    options = Options(payload.options)
    services = Services(payload.services, Service)

    request = amazon.RateRequest(
        shipFrom=amazon.Ship(
            name=payload.shipper.person_name,
            city=payload.shipper.city,
            addressLine1=payload.shipper.address_line1,
            addressLine2=payload.shipper.address_line2,
            stateOrRegion=payload.shipper.state_code,
            email=payload.shipper.email,
            copyEmails=SF.concat_str(payload.shipper.email),
            phoneNumber=payload.shipper.phone_number,
        ),
        shipTo=amazon.Ship(
            name=payload.recipient.person_name,
            city=payload.recipient.city,
            addressLine1=payload.recipient.address_line1,
            addressLine2=payload.recipient.address_line2,
            stateOrRegion=payload.recipient.state_code,
            email=payload.recipient.email,
            copyEmails=SF.concat_str(payload.recipient.email),
            phoneNumber=payload.recipient.phone_number,
        ),
        serviceTypes=list(services),
        shipDate=DF.fdatetime(
            options.shipment_date, "%Y-%m-%d", "%Y-%m-%dT%H:%M:%S.%fZ"
        ),
        containerSpecifications=[
            amazon.ContainerSpecification(
                dimensions=amazon.Dimensions(
                    height=package.height.IN,
                    length=package.length.IN,
                    width=package.width.IN,
                    unit="IN",
                ),
                weight=amazon.Weight(
                    value=package.weight.LB,
                    unit="LB",
                ),
            )
            for package in packages
        ],
    )

    return Serializable(request, DP.to_dict)
