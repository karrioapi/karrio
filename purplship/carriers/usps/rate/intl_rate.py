from typing import Tuple, List
from pyusps.intlratev2request import IntlRateV2Request, PackageType, ExtraServicesType, ContentType
from pyusps.intlratev2response import ServiceType, ExtraServiceType
from purplship.core.utils.helpers import export
from purplship.core.utils.serializable import Serializable
from purplship.core.utils.xml import Element
from purplship.core.models import RateDetails, Error, RateRequest, ChargeDetails
from purplship.core.units import Weight, WeightUnit, Dimension, DimensionUnit, Country
from purplship.carriers.usps.units import IntlContainer, ExtraService, IntlContentType, IntlMailType
from purplship.carriers.usps.error import parse_error_response
from purplship.carriers.usps import Settings


def parse_intl_rate_response(response: Element, settings: Settings) -> Tuple[List[RateDetails], List[Error]]:
    quotes: List[RateDetails] = [
        _extract_intl_rates(package, settings)
        for package in response.xpath(".//*[local-name() = $name]", name="Service",)
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


def intl_rate_request(payload: RateRequest, settings: Settings) -> Serializable[IntlRateV2Request]:
    weight_unit = WeightUnit[payload.shipment.weight_unit or "LB"]
    dimension_unit = DimensionUnit[payload.shipment.dimension_unit or "IN"]
    extra_services = [
        ExtraService[svc.code].value
        for svc in payload.options.keys()
        if svc.code in ExtraService.__members__
    ]
    request = IntlRateV2Request(
        USERID=settings.username,
        Revision="2",
        Package=[
            PackageType(
                ID=item.id or index,
                Pounds=Weight(item.weight, weight_unit).LB,
                Ounces=Weight(item.weight, weight_unit).LB * 16,
                Machinable=None,
                MailType=IntlMailType[item.packaging_type].value,
                GXG=None,
                ValueOfContents=item.value_amount or payload.shipment.declared_value,
                Country=Country[payload.recipient.country_code].value
                if payload.recipient.country_code
                else None,
                Container=(
                    IntlContainer[item.packaging_type].value
                    if item.packaging_type
                    else None
                ),
                Size="LARGE" if any(
                    dim for dim in [
                        Dimension(item.width, dimension_unit).IN,
                        Dimension(item.length, dimension_unit).IN,
                        Dimension(item.height, dimension_unit).IN
                    ] if dim > 12
                ) else "REGULAR",
                Width=Dimension(item.width, dimension_unit).IN,
                Length=Dimension(item.length, dimension_unit).IN,
                Height=Dimension(item.height, dimension_unit).IN,
                Girth=None,
                OriginZip=payload.shipper.postal_code,
                CommercialFlag=None,
                CommercialPlusFlag=None,
                AcceptanceDateTime=payload.shipment.date,
                DestinationPostalCode=payload.recipient.postal_code,
                ExtraServices=None,
                Content=ContentType(
                    ContentType=IntlContentType[item.content].value,
                    ContentDescription=item.content,
                )
                if item.content
                else None,
            )
            for index, item in enumerate(payload.shipment.items)
        ],
    )
    return Serializable(request, _request_serializer)


def _request_serializer(request: IntlRateV2Request) -> dict:
    return {'API': "IntlRateV2", 'XML': export(request)}
