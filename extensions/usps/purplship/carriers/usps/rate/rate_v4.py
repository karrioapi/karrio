from functools import reduce
import attr
from typing import List, Any, Tuple, Optional
from datetime import datetime
from pyusps.ratev4response import PostageType, SpecialServiceType
from pyusps.ratev4request import (
    RateV4Request,
    PackageType,
    SpecialServicesType,
    ShipDateType,
)
from purplship.core.utils import export, Serializable, Element, decimal, to_date
from purplship.core.models import RateDetails, RateRequest, Message, ChargeDetails
from purplship.core.units import Weight, Packages, Currency
from purplship.carriers.usps.utils import Settings
from purplship.carriers.usps.error import parse_error_response
from purplship.carriers.usps.units import (
    Service,
    FirstClassMailType,
    Size,
    SpecialService,
)

REQUIRED_MAIL_TYPE_SERVICES = [
    Service.first_class,
    Service.first_class_commercial,
    Service.first_class_hfp_commercial,
]


def parse_rate_v4_response(
    response: Element, settings: Settings
) -> Tuple[List[RateDetails], List[Message]]:
    rates: List[RateDetails] = [
        _extract_quote(package, settings)
        for package in response.xpath(".//*[local-name() = $name]", name="Postage")
    ]
    return rates, parse_error_response(response, settings)


def _extract_quote(postage_node: Element, settings: Settings) -> RateDetails:
    postage: PostageType = PostageType()
    postage.build(postage_node)
    currency = Currency.USD.name
    services: List[SpecialServiceType] = [
        (lambda s: (s, s.build(svc)))(SpecialServiceType())[0]
        for svc in postage_node.xpath(
            ".//*[local-name() = $name]", name="SpecialService"
        )
    ]
    estimated_date = to_date(postage.CommitmentDate)
    transit = (
        (estimated_date - datetime.now()).days if estimated_date is not None else None
    )

    def get(key: str) -> Any:
        return reduce(lambda r, v: v.text, postage_node.findall(key), None)

    return RateDetails(
        carrier_name=settings.carrier_name,
        carrier_id=settings.carrier_id,
        service=get("MailService"),
        total_charge=decimal(postage_node.find("Rate").text),
        currency=currency,
        transit_days=transit,
        extra_charges=[
            ChargeDetails(
                name=SpecialService(str(svc.ServiceID)).name,
                amount=decimal(svc.Price),
                currency=currency,
            )
            for svc in services
        ],
    )


def rate_v4_request(
    request_payload: RateRequest, settings: Settings
) -> Serializable[RateV4Request]:
    payload = RateRequestExtensionV4(request_payload)
    request = RateV4Request(
        USERID=settings.username,
        Revision="2",
        Package=[
            PackageType(
                ID=payload.package.parcel.id,
                SortationLevel=None,
                DestinationEntryFacilityType=None,
                Nonprofit=None,
                Service=payload.service,
                FirstClassMailType=payload.mail_type,
                ZipOrigination=payload.shipper.postal_code,
                ZipDestination=payload.recipient.postal_code,
                Pounds=payload.package.weight.LB,
                Ounces=payload.package.weight.OZ,
                Container=payload.container,
                Size=payload.size,
                Width=payload.package.width.IN,
                Length=payload.package.length.IN,
                Height=payload.package.height.IN,
                Girth=payload.package.girth.value,
                Value=None,
                AmountToCollect=None,  # TODO:: compute this with COD option
                SpecialServices=SpecialServicesType(
                    SpecialService=payload.special_services.keys()
                )
                if payload.special_services is not None
                else None,
                Content=None,
                GroundOnly=None,
                SortBy=None,
                Machinable=None,
                ReturnLocations=None,
                ReturnServiceInfo=None,
                DropOffTime=None,
                ShipDate=ShipDateType(
                    Option=None, valueOf_=str(datetime.today().strftime("%Y-%m-%d"))
                ),
            )
        ],
    )
    return Serializable(request, _request_serializer)


def _request_serializer(request: RateV4Request) -> dict:
    return {"API": "RateV4", "XML": export(request)}


@attr.s(auto_attribs=True)
class RateRequestExtensionV4:
    request: RateRequest

    @property
    def package(self):
        return Packages(self.request.parcels).single

    @property
    def shipper(self):
        return self.request.shipper

    @property
    def recipient(self):
        return self.request.recipient

    @property
    def options(self):
        return self.request.options

    @property
    def service(self):
        return next(
            (
                Service[s].value
                for s in self.request.services
                if s in Service.__members__
            ),
            Service.first_class.value,
        )

    @property
    def mail_type(self):
        return (
            FirstClassMailType[self.package.packaging_type or "small_box"].value
            if Service(self.service) in REQUIRED_MAIL_TYPE_SERVICES
            else None
        )

    @property
    def size(self):
        dimensions = [self.package.width.value, self.package.length.value, self.package.height.value]
        dimension_above_12_in = any(dim for dim in dimensions if dim and dim > 12)
        return Size.large.value if dimension_above_12_in else Size.regular.value

    @property
    def container(self):
        return None

    @property
    def girth(self):
        return None

    @property
    def machinable(self):
        return None

    @property
    def special_services(self) -> Optional[dict]:
        options = {}
        for option, value in self.options.items():
            if option in SpecialService.__members__:
                options.update({SpecialService[option].value: True})

        return options if len(options) > 0 else None
