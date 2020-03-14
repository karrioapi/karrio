from typing import Tuple, List
from datetime import datetime
from pyusps.intlratev2request import IntlRateV2Request, PackageType
from pyusps.intlratev2response import ServiceType, ExtraServiceType
from purplship.core.utils.helpers import export
from purplship.core.utils.serializable import Serializable
from purplship.core.utils.xml import Element
from purplship.core.models import RateDetails, Error, RateRequest, ChargeDetails
from purplship.core.units import Weight, WeightUnit, Dimension, DimensionUnit, Country
from purplship.carriers.usps.units import IntlContainer, ExtraService, IntlMailType
from purplship.carriers.usps.error import parse_error_response
from purplship.carriers.usps import Settings


def parse_intl_rate_response(
    response: Element, settings: Settings
) -> Tuple[List[RateDetails], List[Error]]:
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
    return RateDetails(
        carrier=settings.carrier_name,
        service_name=None,
        service_type=service.MailType,
        base_charge=None,
        duties_and_taxes=None,
        total_charge=service.Postage,
        currency=currency,
        delivery_date=service.GuaranteeAvailability,
        discount=None,
        extra_charges=[
            ChargeDetails(
                name=ExtraService(special.ServiceID).name,
                amount=special.Price,
                currency=currency,
            )
            for special in special_services
        ],
    )


def intl_rate_request(
    payload: RateRequest, settings: Settings
) -> Serializable[IntlRateV2Request]:
    weight_unit = WeightUnit[payload.parcel.weight_unit or "LB"]
    dimension_unit = DimensionUnit[payload.parcel.dimension_unit or "IN"]
    request = IntlRateV2Request(
        USERID=settings.username,
        Revision="2",
        Package=[
            PackageType(
                ID=payload.parcel.id or 1,
                Pounds=Weight(payload.parcel.weight, weight_unit).LB,
                Ounces=Weight(payload.parcel.weight, weight_unit).LB * 16,
                Machinable=None,
                MailType=IntlMailType[payload.parcel.packaging_type].value,
                GXG=None,
                ValueOfContents=None,
                Country=(
                    Country[payload.recipient.country_code].value
                    if payload.recipient.country_code
                    else None
                ),
                Container=(
                    IntlContainer[payload.parcel.packaging_type].value
                    if payload.parcel.packaging_type
                    else None
                ),
                Size="LARGE"
                if any(
                    dim
                    for dim in [
                        Dimension(payload.parcel.width, dimension_unit).IN,
                        Dimension(payload.parcel.length, dimension_unit).IN,
                        Dimension(payload.parcel.height, dimension_unit).IN,
                    ]
                    if dim > 12
                )
                else "REGULAR",
                Width=Dimension(payload.parcel.width, dimension_unit).IN,
                Length=Dimension(payload.parcel.length, dimension_unit).IN,
                Height=Dimension(payload.parcel.height, dimension_unit).IN,
                Girth=None,
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
