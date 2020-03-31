from functools import reduce
from typing import List, Tuple
from pyups import common
from pyups.freight_rate_web_service_schema import (
    FreightRateRequest,
    FreightRateResponse,
    ShipFromType,
    AddressType,
    ShipToType,
    RateCodeDescriptionType,
    HandlingUnitType,
    ShipmentServiceOptionsType,
    PickupOptionsType,
    WeightType,
    UnitOfMeasurementType,
    CommodityType,
    DimensionsType,
)
from purplship.core.utils.helpers import export, concat_str
from purplship.core.utils.serializable import Serializable
from purplship.core.utils.soap import clean_namespaces, create_envelope
from purplship.core.units import DimensionUnit, Dimension, Weight, WeightUnit
from purplship.core.utils.xml import Element
from purplship.core.models import RateDetails, Message, ChargeDetails, RateRequest
from purplship.carriers.ups.units import (
    RatingServiceCode,
    WeightUnit as UPSWeightUnit,
    FreightPackagingType,
)
from purplship.carriers.ups.error import parse_error_response
from purplship.carriers.ups.utils import Settings


def parse_freight_rate_response(
    response: Element, settings: Settings
) -> Tuple[List[RateDetails], List[Message]]:
    rate_reply = response.xpath(
        ".//*[local-name() = $name]", name="FreightRateResponse"
    )
    rates: List[RateDetails] = [
        _extract_freight_rate(detail_node, settings) for detail_node in rate_reply
    ]
    return rates, parse_error_response(response, settings)


def _extract_freight_rate(detail_node: Element, settings: Settings) -> RateDetails:
    detail = FreightRateResponse()
    detail.build(detail_node)

    total_charge = [r for r in detail.Rate if r.Type.Code == "AFTR_DSCNT"][0]
    Discounts_ = [
        ChargeDetails(
            name=r.Type.Code,
            currency=r.Factor.UnitOfMeasurement.Code,
            amount=float(r.Factor.Value),
        )
        for r in detail.Rate
        if r.Type.Code == "DSCNT"
    ]
    Surcharges_ = [
        ChargeDetails(
            name=r.Type.Code,
            currency=r.Factor.UnitOfMeasurement.Code,
            amount=float(r.Factor.Value),
        )
        for r in detail.Rate
        if r.Type.Code not in ["DSCNT", "AFTR_DSCNT", "DSCNT_RATE", "LND_GROSS"]
    ]
    extra_charges = Discounts_ + Surcharges_
    currency_ = next(
        c.text
        for c in detail_node.xpath(".//*[local-name() = $name]", name="CurrencyCode")
    )
    return RateDetails(
        carrier=settings.carrier,
        carrier_name=settings.carrier_name,
        currency=currency_,
        service=detail.Service.Description,
        base_charge=float(detail.TotalShipmentCharge.MonetaryValue),
        total_charge=float(total_charge.Factor.Value or 0.0),
        duties_and_taxes=reduce(lambda r, c: r + c.amount, Surcharges_, 0.0),
        discount=reduce(lambda r, c: r + c.amount, Discounts_, 0.0),
        extra_charges=extra_charges,
    )


def freight_rate_request(
    payload: RateRequest, settings: Settings
) -> Serializable[FreightRateRequest]:
    dimension_unit = DimensionUnit[payload.parcel.dimension_unit or "IN"]
    weight_unit = WeightUnit[payload.parcel.weight_unit or "LB"]
    service = (
        [
            RatingServiceCode[svc]
            for svc in payload.parcel.services
            if svc in RatingServiceCode.__members__
        ]
        + [RatingServiceCode.ups_freight_ltl_guaranteed]
    )[0]
    request = FreightRateRequest(
        Request=common.RequestType(
            TransactionReference=common.TransactionReferenceType(
                TransactionIdentifier="TransactionIdentifier"
            ),
            RequestOption=[1],
        ),
        ShipFrom=ShipFromType(
            Name=payload.shipper.company_name,
            Address=AddressType(
                AddressLine=concat_str(
                    payload.shipper.address_line1, payload.shipper.address_line2
                ),
                City=payload.shipper.city,
                PostalCode=payload.shipper.postal_code,
                CountryCode=payload.shipper.country_code,
                StateProvinceCode=payload.shipper.state_code,
            ),
            AttentionName=payload.shipper.person_name,
        ),
        ShipTo=ShipToType(
            Name=payload.recipient.company_name,
            Address=AddressType(
                AddressLine=concat_str(
                    payload.recipient.address_line1, payload.recipient.address_line2
                ),
                City=payload.recipient.city,
                PostalCode=payload.recipient.postal_code,
                CountryCode=payload.recipient.country_code,
                StateProvinceCode=payload.recipient.state_code,
            ),
            AttentionName=payload.recipient.person_name,
        ),
        PaymentInformation=None,
        Service=RateCodeDescriptionType(Code=service.value, Description=None),
        HandlingUnitOne=HandlingUnitType(
            Quantity=1, Type=RateCodeDescriptionType(Code="SKD")
        ),
        ShipmentServiceOptions=ShipmentServiceOptionsType(
            PickupOptions=PickupOptionsType(WeekendPickupIndicator="")
        ),
        DensityEligibleIndicator="",
        AdjustedWeightIndicator="",
        HandlingUnitWeight=None,
        PickupRequest=None,
        GFPOptions=None,
        TimeInTransitIndicator="",
        Commodity=[
            CommodityType(
                Description=payload.parcel.description or "...",
                Weight=WeightType(
                    UnitOfMeasurement=UnitOfMeasurementType(
                        Code=UPSWeightUnit[weight_unit.name].value
                    ),
                    Value=Weight(payload.parcel.weight, weight_unit).value,
                ),
                Dimensions=DimensionsType(
                    UnitOfMeasurement=UnitOfMeasurementType(Code=dimension_unit.value),
                    Width=Dimension(payload.parcel.width, dimension_unit).value,
                    Height=Dimension(payload.parcel.height, dimension_unit).value,
                    Length=Dimension(payload.parcel.length, dimension_unit).value,
                ),
                NumberOfPieces=None,
                PackagingType=RateCodeDescriptionType(
                    Code=FreightPackagingType[payload.parcel.packaging_type or "small_box"].value,
                    Description=None,
                ),
                FreightClass=50,
            )
        ],
    )
    return Serializable(
        create_envelope(header_content=settings.Security, body_content=request),
        _request_serializer,
    )


def _request_serializer(request: Element) -> str:
    namespace_ = """
        xmlns:tns="http://schemas.xmlsoap.org/soap/envelope/"
        xmlns:xsd="http://www.w3.org/2001/XMLSchema"
        xmlns:upss="http://www.ups.com/XMLSchema/XOLTWS/UPSS/v1.0"
        xmlns:wsf="http://www.ups.com/schema/wsf"
        xmlns:common="http://www.ups.com/XMLSchema/XOLTWS/Common/v1.0"
        xmlns:frt="http://www.ups.com/XMLSchema/XOLTWS/FreightRate/v1.0"
    """.replace(
        " ", ""
    ).replace(
        "\n", " "
    )
    return clean_namespaces(
        export(request, namespacedef_=namespace_),
        envelope_prefix="tns:",
        header_child_prefix="upss:",
        header_child_name="UPSSecurity",
        body_child_name="FreightRateRequest",
        body_child_prefix="frt:",
    ).replace("common:Code", "rate:Code")
