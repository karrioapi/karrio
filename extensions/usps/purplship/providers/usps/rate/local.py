from functools import reduce
from typing import List, Any, Tuple
from datetime import datetime
from usps_lib.rate_v4_response import PostageType, SpecialServiceType
from usps_lib.rate_v4_request import (
    RateV4Request,
    PackageType,
    SpecialServicesType,
    ShipDateType,
)
from purplship.core.utils import Serializable, Element, NF, XP, DF
from purplship.core.models import RateDetails, RateRequest, Message, ChargeDetails
from purplship.core.units import Packages, Currency, Options, Services
from purplship.providers.usps.utils import Settings
from purplship.providers.usps.error import parse_error_response
from purplship.providers.usps.units import (
    Container,
    FirstClassMailType,
    RateService,
    Service,
    Size,
    SpecialService,
)


def parse_rate_response(response: Element, settings: Settings) -> Tuple[List[RateDetails], List[Message]]:
    rates: List[RateDetails] = [
        _extract_details(package, settings)
        for package in response.xpath(".//*[local-name() = $name]", name="Postage")
    ]
    return rates, parse_error_response(response, settings)


def _extract_details(postage_node: Element, settings: Settings) -> RateDetails:
    postage: PostageType = PostageType()
    postage.build(postage_node)
    currency = Currency.USD.name
    services: List[SpecialServiceType] = [
        XP.build(SpecialServiceType, svc)
        for svc in postage_node.xpath(
            ".//*[local-name() = $name]", name="SpecialService"
        )
    ]
    estimated_date = DF.date(postage.CommitmentDate)
    transit = (
        (estimated_date - datetime.now()).days if estimated_date is not None else None
    )
    postage_rate = postage_node.find("Rate").text

    def get(key: str) -> Any:
        return reduce(lambda r, v: v.text, postage_node.findall(key), None)

    return RateDetails(
        carrier_name=settings.carrier_name,
        carrier_id=settings.carrier_id,
        service=Service.find(get("MailService")).name,
        total_charge=NF.decimal(postage_rate),
        currency=currency,
        transit_days=transit,
        extra_charges=[
            ChargeDetails(
                name=SpecialService(str(svc.ServiceID)).name,
                amount=NF.decimal(svc.Price),
                currency=currency,
            )
            for svc in services
        ],
    )


def rate_request(payload: RateRequest, settings: Settings) -> Serializable[RateV4Request]:
    package = Packages(payload.parcels).single
    options = Options(payload.options)
    service = Services(payload.services, RateService).first or RateService.usps_all
    special_services = Services(payload.options.keys(), SpecialService)

    request = RateV4Request(
        USERID=settings.username,
        Revision="2",
        Package=[
            PackageType(
                ID=0,
                Service=service.value,
                FirstClassMailType=FirstClassMailType[package.packaging_type or "your_packaging"].value,
                ZipOrigination=payload.shipper.postal_code,
                ZipDestination=payload.recipient.postal_code,
                Pounds=package.weight.LB,
                Ounces=package.weight.OZ,
                Container=Container[package.packaging_type or "your_packaging"].value,
                Width=package.width.IN,
                Length=package.length.IN,
                Height=package.height.IN,
                Girth=package.girth.value,
                Value=None,
                AmountToCollect=options.cash_on_delivery,
                SpecialServices=SpecialServicesType(
                    SpecialService=[s.value for s in special_services]
                ),
                Content=None,
                GroundOnly=None,
                SortBy=None,
                Machinable=("usps_machinable" in options),
                ReturnLocations=None,
                ReturnServiceInfo=None,
                DropOffTime=None,
                ShipDate=ShipDateType(
                    valueOf_=str(datetime.today().strftime("%Y-%m-%d"))
                ),
            )
        ],
    )

    return Serializable(request, XP.export)
