from functools import reduce
from typing import List, Any
from pyusps.ratev4request import RateV4Request, PackageType, SpecialServicesType
from pyusps.ratev4response import PostageType, SpecialServiceType
from purplship.core.utils.helpers import export
from purplship.core.utils.serializable import Serializable
from purplship.core.utils.xml import Element
from purplship.core.models import RateDetails, Error, RateRequest, ChargeDetails
from purplship.core.units import Weight, WeightUnit, Dimension, DimensionUnit, Currency
from purplship.carriers.usps.units import SpecialService, Container, Service, FirstClassMailType
from purplship.carriers.usps.error import parse_error_response
from purplship.carriers.usps import Settings


def parse_rate_v4_response(response: Element, settings: Settings) -> (List[RateDetails], List[Error]):
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
    weight_unit = WeightUnit[payload.shipment.weight_unit or "LB"]
    dimension_unit = DimensionUnit[payload.shipment.dimension_unit or "IN"]
    request = RateV4Request(
        USERID=settings.username,
        Revision="2",
        Package=[
            (lambda weight, width, length, height, item_services, item_special_services: PackageType(
                ID=item.id or str(index),
                DestinationEntryFacilityType=None,
                SortationLevel=None,
                Service=(
                    lambda item_services: ", ".join(
                        [Service[svc].value for svc in item_services]
                    )
                    if len(item_services) > 0
                    else None
                )(list(set(item_services))),
                FirstClassMailType=FirstClassMailType[item.packaging_type].value
                if (
                    item.packaging_type is not None
                    and any(
                        svc
                        for svc in item_services
                        if Service[svc].value
                        in ["First Class", "First Class Commercial", "First Class HFPCommercial"]
                    )
                )
                else None,
                ZipOrigination=payload.shipper.postal_code,
                ZipDestination=payload.recipient.postal_code,
                Pounds=weight,
                Ounces=weight * 16,
                Container=(
                    Container[item.packaging_type].value
                    if item.packaging_type
                    else None
                ),
                Size=Z(
                    "LARGE"
                    if any(dim for dim in [width, length, height] if dim and dim > 12) else
                    "REGULAR"
                ),
                Width=width,
                Length=length,
                Height=height,
                Girth=None,
                Value=item.value_amount,
                AmountToCollect=None,
                SpecialServices=SpecialServicesType(
                    SpecialService=[
                        SpecialService[svc].value
                        for svc in item_special_services
                    ]
                )
                if len(item_special_services) > 0
                else None,
                Content=None,
                GroundOnly=None,
                SortBy=None,
                Machinable=None,
                ReturnLocations=None,
                ReturnServiceInfo=None,
                DropOffTime=None,
                ShipDate=payload.shipment.date,
            ))(
                round(Weight(item.weight, weight_unit).LB),  # weight
                Dimension(item.width, dimension_unit).IN,  # width
                Dimension(item.length, dimension_unit).IN,  # length
                Dimension(item.height, dimension_unit).IN,  # height
                [],  # item_services
                []  # item_special_services
            )
            for index, item in enumerate(payload.shipment.items)
        ],
    )
    return Serializable(request, _request_serializer)


def _request_serializer(request: RateV4Request) -> dict:
    return {'API': "RateV4", 'XML': export(request)}
