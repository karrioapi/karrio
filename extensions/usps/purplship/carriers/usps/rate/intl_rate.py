from typing import Tuple, List
from datetime import datetime
from pyusps.intlratev2request import IntlRateV2Request, PackageType
from pyusps.intlratev2response import ServiceType, ExtraServiceType
from purplship.core.utils import export, Serializable, Element, decimal, to_date
from purplship.core.models import RateDetails, Message, RateRequest, ChargeDetails
from purplship.core.units import Packages, Country
from purplship.carriers.usps.units import IntlContainer, ExtraService, IntlMailType
from purplship.carriers.usps.error import parse_error_response
from purplship.carriers.usps import Settings


def parse_intl_rate_response(
    response: Element, settings: Settings
) -> Tuple[List[RateDetails], List[Message]]:
    quotes: List[RateDetails] = [
        _extract_intl_rates(package, settings)
        for package in response.xpath(".//*[local-name() = $name]", name="Service")
    ]
    return quotes, parse_error_response(response, settings)


def _extract_intl_rates(service_node: Element, settings: Settings) -> RateDetails:
    service: ServiceType = ServiceType()
    service.build(service_node)
    currency = "USD"
    special_services: List[ExtraServiceType] = [
        (lambda s: (s, s.build(svc)))(ExtraServiceType())[0]
        for svc in service_node.xpath(".//*[local-name() = $name]", name="ExtraService")
    ]
    delivery_date = to_date(service.GuaranteeAvailability, "%m/%d/%Y")
    transit = (
        (delivery_date - datetime.now()).days if delivery_date is not None else None
    )

    return RateDetails(
        carrier_name=settings.carrier_name,
        carrier_id=settings.carrier_id,
        service=service.SvcDescription,
        base_charge=decimal(service.Postage),
        total_charge=decimal(service.Postage),
        currency=currency,
        transit_days=transit,
        extra_charges=[
            ChargeDetails(
                name=ExtraService(special.ServiceID).name,
                amount=decimal(special.Price),
                currency=currency,
            )
            for special in special_services
        ],
    )


def intl_rate_request(
    payload: RateRequest, settings: Settings
) -> Serializable[IntlRateV2Request]:
    package = Packages(payload.parcels).single
    request = IntlRateV2Request(
        USERID=settings.username,
        Revision="2",
        Package=[
            PackageType(
                ID=package.parcel.id or 1,
                Pounds=package.weight.LB,
                Ounces=package.weight.OZ,
                Machinable=None,
                MailType=IntlMailType[package.packaging_type].value,
                GXG=None,
                ValueOfContents=None,
                Country=(
                    Country[payload.recipient.country_code].value
                    if payload.recipient.country_code
                    else None
                ),
                Container=(
                    IntlContainer[package.packaging_type].value
                    if package.packaging_type
                    else None
                ),
                Size="LARGE"
                if any(
                    dim
                    for dim in [
                        package.width.IN,
                        package.length.IN,
                        package.height.IN,
                    ]
                    if dim > 12
                )
                else "REGULAR",
                Width=package.width.IN,
                Length=package.length.IN,
                Height=package.height.IN,
                Girth=package.girth.value,
                OriginZip=payload.shipper.postal_code,
                CommercialFlag=None,
                CommercialPlusFlag=None,
                AcceptanceDateTime=datetime.today().strftime("%Y-%m-%dT%H:%M:%S"),
                DestinationPostalCode=payload.recipient.postal_code,
                ExtraServices=None,
                Content=None,
            )
        ],
    )
    return Serializable(request, _request_serializer)


def _request_serializer(request: IntlRateV2Request) -> dict:
    return {"API": "IntlRateV2", "XML": export(request)}
