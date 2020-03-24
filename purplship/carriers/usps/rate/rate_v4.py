from functools import reduce
import attr
from typing import List, Any, Tuple, Optional
from datetime import datetime
from pyusps.ratev4response import PostageType, SpecialServiceType
from pyusps.ratev4request import (
    RateV4Request, PackageType, SpecialServicesType, ShipDateType
)
from purplship.core.utils.helpers import export
from purplship.core.utils.serializable import Serializable
from purplship.core.utils.xml import Element
from purplship.core.models import RateDetails, RateRequest, Error, ChargeDetails
from purplship.core.units import Weight, WeightUnit, Dimension, DimensionUnit, Currency
from purplship.carriers.usps.utils import Settings
from purplship.carriers.usps.error import parse_error_response
from purplship.carriers.usps.units import Service, FirstClassMailType, Size, SpecialService

REQUIRED_MAIL_TYPE_SERVICES = [Service.first_class, Service.first_class_commercial, Service.first_class_hfp_commercial]


def parse_rate_v4_response(
    response: Element, settings: Settings
) -> Tuple[List[RateDetails], List[Error]]:
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

    def get(key: str) -> Any:
        return reduce(lambda r, v: v.text, postage_node.findall(key), None)

    return RateDetails(
        carrier=settings.carrier_name,
        service=get("MailService"),
        total_charge=float(postage_node.find("Rate").text),
        currency=currency,
        estimated_delivery=postage.CommitmentDate,
        extra_charges=[
            ChargeDetails(
                name=SpecialService(str(svc.ServiceID)).name,
                amount=svc.Price,
                currency=currency,
            )
            for svc in services
        ],
    )


def rate_v4_request(request_payload: RateRequest, settings: Settings) -> Serializable[RateV4Request]:
    payload = RateRequestExtensionV4(request_payload)
    request = RateV4Request(
        USERID=settings.username,
        Revision='2',
        Package=[
            PackageType(
                ID=payload.parcel.id,
                SortationLevel=None,
                DestinationEntryFacilityType=None,
                Nonprofit=None,
                Service=payload.service,
                FirstClassMailType=payload.mail_type,
                ZipOrigination=payload.shipper.postal_code,
                ZipDestination=payload.recipient.postal_code,
                Pounds=payload.weight.LB,
                Ounces=payload.weight.OZ,
                Container=payload.container,
                Size=payload.size,
                Width=payload.width,
                Length=payload.length,
                Height=payload.height,
                Girth=payload.girth,
                Value=None,
                AmountToCollect=None,  # TODO:: compute this with COD option
                SpecialServices=SpecialServicesType(
                    SpecialService=payload.options.keys()
                ) if payload.options is not None else None,
                Content=None,
                GroundOnly=None,
                SortBy=None,
                Machinable=None,
                ReturnLocations=None,
                ReturnServiceInfo=None,
                DropOffTime=None,
                ShipDate=ShipDateType(
                    Option=None,
                    valueOf_=str(datetime.today().strftime("%Y-%m-%d"))
                ),
            )
        ]
    )
    return Serializable(request, _request_serializer)


def _request_serializer(request: RateV4Request) -> dict:
    return {"API": "RateV4", "XML": export(request)}


@attr.s(auto_attribs=True)
class RateRequestExtensionV4:
    request: RateRequest

    @property
    def parcel(self):
        return self.request.parcel

    @property
    def shipper(self):
        return self.request.shipper

    @property
    def recipient(self):
        return self.request.recipient

    @property
    def dimension_unit(self):
        return DimensionUnit[self.parcel.dimension_unit or "IN"]

    @property
    def weight_unit(self):
        return WeightUnit[self.parcel.weight_unit or "LB"]

    @property
    def weight(self):
        return Weight(self.parcel.weight, self.weight_unit)

    @property
    def width(self):
        return Dimension(self.parcel.width, self.dimension_unit).IN

    @property
    def height(self):
        return Dimension(self.parcel.height, self.dimension_unit).IN

    @property
    def length(self):
        return Dimension(self.parcel.length, self.dimension_unit).IN

    @property
    def service(self):
        return next(
            (Service[s].value for s in self.parcel.services if s in Service.__members__),
            Service.first_class.value
        )

    @property
    def mail_type(self):
        return (
            FirstClassMailType[self.parcel.packaging_type or "small_box"].value
            if Service(self.service) in REQUIRED_MAIL_TYPE_SERVICES else None
        )

    @property
    def size(self):
        dimensions = [self.width, self.length, self.height]
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
    def options(self) -> Optional[dict]:
        options = {}
        for option, value in self.parcel.options.items():
            if option in SpecialService.__members__:
                options.update({SpecialService[option].value: True})

        return options if len(options) > 0 else None
