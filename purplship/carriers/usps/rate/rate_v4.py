from functools import reduce
from typing import List, Any, Tuple
from datetime import datetime
from pyusps.ratev4request import RateV4Request, PackageType, ShipDateType
from pyusps.ratev4response import PostageType, SpecialServiceType
from purplship.core.utils.helpers import export
from purplship.core.utils.serializable import Serializable
from purplship.core.utils.xml import Element
from purplship.core.models import RateDetails, Error, RateRequest, ChargeDetails
from purplship.core.units import Weight, WeightUnit, Dimension, DimensionUnit, Currency
from purplship.carriers.usps.units import SpecialService, Container
from purplship.carriers.usps.error import parse_error_response
from purplship.carriers.usps import Settings


def parse_rate_v4_response(response: Element, settings: Settings) -> Tuple[List[RateDetails], List[Error]]:
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
        service_name=None,
        service_type=get("MailService"),
        base_charge=None,
        duties_and_taxes=None,
        total_charge=float(postage_node.find("Rate").text),
        currency=currency,
        delivery_date=postage.CommitmentDate,
        discount=None,
        extra_charges=[
            ChargeDetails(
                name=SpecialService(str(svc.ServiceID)).name,
                amount=svc.Price,
                currency=currency,
            )
            for svc in services
        ],
    )


def rate_v4_request(payload: RateRequest, settings: Settings) -> Serializable[RateV4Request]:
    weight_unit = WeightUnit[payload.parcel.weight_unit or "LB"]
    dimension_unit = DimensionUnit[payload.parcel.dimension_unit or "IN"]
    request = RateV4Request(
        USERID=settings.username,
        Revision="2",
        Package=[
            PackageType(
                ID=payload.parcel.id or "1",
                DestinationEntryFacilityType=None,
                SortationLevel=None,
                Service=None,
                FirstClassMailType=None,
                ZipOrigination=payload.shipper.postal_code,
                ZipDestination=payload.recipient.postal_code,
                Pounds=Weight(payload.parcel.weight, weight_unit).LB,
                Ounces=Weight(payload.parcel.weight, weight_unit).LB * 16,
                Container=(
                    Container[payload.parcel.packaging_type].value
                    if payload.parcel.packaging_type
                    else None
                ),
                Size="LARGE" if any(
                    dim for dim in [
                        Dimension(payload.parcel.width, dimension_unit).IN,
                        Dimension(payload.parcel.length, dimension_unit).IN,
                        Dimension(payload.parcel.height, dimension_unit).IN
                    ] if dim > 12
                ) else "REGULAR",
                Width=Dimension(payload.parcel.width, dimension_unit).IN,
                Length=Dimension(payload.parcel.length, dimension_unit).IN,
                Height=Dimension(payload.parcel.height, dimension_unit).IN,
                Girth=None,
                Value=None,
                AmountToCollect=None,
                SpecialServices=None,
                Content=None,
                GroundOnly=None,
                SortBy=None,
                Machinable=None,
                ReturnLocations=None,
                ReturnServiceInfo=None,
                DropOffTime=None,
                ShipDate=ShipDateType(valueOf_=datetime.today().strftime('%Y-%m-%d')),
            )
        ],
    )
    return Serializable(request, _request_serializer)


def _request_serializer(request: RateV4Request) -> dict:
    return {'API': "RateV4", 'XML': export(request)}
