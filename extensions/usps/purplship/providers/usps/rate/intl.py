from typing import Tuple, List
from datetime import datetime
from usps_lib.intl_rate_v2_request import IntlRateV2Request, PackageType, ExtraServicesType
from usps_lib.intl_rate_v2_response import ServiceType, ExtraServiceType
from purplship.core.utils import Serializable, Element, NF, XP, DF
from purplship.core.models import RateDetails, Message, RateRequest, ChargeDetails
from purplship.core.units import Packages, Country, Weight, WeightUnit, Services

from purplship.providers.usps.units import RateService, ExtraService, IntlPackageType, Service
from purplship.providers.usps.error import parse_error_response
from purplship.providers.usps import Settings


def parse_rate_response(response: Element, settings: Settings) -> Tuple[List[RateDetails], List[Message]]:
    quotes: List[RateDetails] = [
        _extract_details(package, settings)
        for package in response.xpath(".//*[local-name() = $name]", name="Service")
    ]
    return quotes, parse_error_response(response, settings)


def _extract_details(service_node: Element, settings: Settings) -> RateDetails:
    service: ServiceType = ServiceType()
    service.build(service_node)
    currency = "USD"
    special_services: List[ExtraServiceType] = [
        XP.build(ExtraServiceType, svc)
        for svc in service_node.xpath(".//*[local-name() = $name]", name="ExtraService")
    ]
    delivery_date = DF.date(service.GuaranteeAvailability, "%m/%d/%Y")
    transit = (
        (delivery_date - datetime.now()).days if delivery_date is not None else None
    )
    rate_service: Service = Service.find(service.SvcDescription)

    return RateDetails(
        carrier_name=settings.carrier_name,
        carrier_id=settings.carrier_id,
        service=rate_service.value,
        base_charge=NF.decimal(service.Postage),
        total_charge=NF.decimal(service.Postage),
        currency=currency,
        transit_days=transit,
        extra_charges=[
            ChargeDetails(
                name=ExtraService(special.ServiceID).name,
                amount=NF.decimal(special.Price),
                currency=currency,
            )
            for special in special_services
        ],
    )


def rate_request(payload: RateRequest, settings: Settings) -> Serializable[IntlRateV2Request]:
    package = Packages(payload.parcels, max_weight=Weight(70, WeightUnit.LB)).single
    services = Services(payload.options.keys(), RateService)
    extra_services = Services(payload.services, ExtraService)

    commercial = "Y" if "commercial" in services else "N"
    commercial_plus = "Y" if "plus" in services else "N"
    country = (
        Country[payload.recipient.country_code].value
        if payload.recipient.country_code else None
    )

    request = IntlRateV2Request(
        USERID=settings.username,
        Revision="2",
        Package=[
            PackageType(
                ID=0,
                Pounds=package.weight.LB,
                Ounces=package.weight.OZ,
                Machinable=("usps_machinable" in payload.options),
                MailType=IntlPackageType[package.packaging_type or "package"].value,
                GXG=None,
                ValueOfContents=None,
                Country=country,
                Width=package.width.IN,
                Length=package.length.IN,
                Height=package.height.IN,
                Girth=(package.girth.value if package.packaging_type == "tube" else None),
                OriginZip=payload.shipper.postal_code,
                CommercialFlag=commercial,
                CommercialPlusFlag=commercial_plus,
                AcceptanceDateTime=datetime.today().strftime("%Y-%m-%dT%H:%M:%S"),
                DestinationPostalCode=payload.recipient.postal_code,
                ExtraServices=ExtraServicesType(
                    ExtraService=[s.value for s in extra_services]
                ),
                Content=None,
            )
        ],
    )

    return Serializable(request, XP.export)
