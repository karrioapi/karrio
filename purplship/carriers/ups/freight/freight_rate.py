from functools import reduce, partial
from typing import List, Tuple
from pyups import common
from pyups.freight_rate_web_service_schema import (
    FreightRateRequest, FreightRateResponse, ShipFromType, AddressType,
    ShipToType, PaymentInformationType, PayerType, RateCodeDescriptionType,
    HandlingUnitType, ShipmentServiceOptionsType, PickupOptionsType, WeightType,
    HandlingUnitWeightType, UnitOfMeasurementType, CommodityType, OnCallInformationType,
    DimensionsType
)
from purplship.core.utils.helpers import export
from purplship.core.utils.serializable import Serializable
from purplship.core.utils.soap import clean_namespaces, create_envelope
from purplship.core.units import DimensionUnit
from purplship.core.utils.xml import Element
from purplship.core.models import RateDetails, Error, ChargeDetails, RateRequest
from purplship.carriers.ups.units import RatingServiceCode, WeightUnit, PackagingType
from purplship.carriers.ups.error import parse_error_response
from purplship.carriers.ups.utils import Settings


def parse_freight_rate_response(response: Element, settings: Settings) -> Tuple[List[RateDetails], List[Error]]:
    rate_reply = response.xpath(".//*[local-name() = $name]", name="FreightRateResponse")
    rates: List[RateDetails] = [_extract_freight_rate(detail_node, settings) for detail_node in rate_reply]
    return rates, parse_error_response(response)


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
    currency_ = next(c.text for c in detail_node.xpath(".//*[local-name() = $name]", name="CurrencyCode"))
    return RateDetails(
        carrier=settings.carrier_name,
        currency=currency_,
        service_name=detail.Service.Description,
        service_type=detail.Service.Code,
        base_charge=float(detail.TotalShipmentCharge.MonetaryValue),
        total_charge=float(total_charge.Factor.Value or 0.0),
        duties_and_taxes=reduce(lambda r, c: r + c.amount, Surcharges_, 0.0),
        discount=reduce(lambda r, c: r + c.amount, Discounts_, 0.0),
        extra_charges=extra_charges,
    )


def freight_rate_request(payload: RateRequest, settings: Settings) -> Serializable[FreightRateRequest]:
    service = (
        [
            RatingServiceCode[svc]
            for svc in payload.shipment.services
            if svc in RatingServiceCode.__members__
        ]
        + [RatingServiceCode.UPS_Freight_LTL_Guaranteed]
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
                AddressLine=payload.shipper.address_lines,
                City=payload.shipper.city,
                PostalCode=payload.shipper.postal_code,
                CountryCode=payload.shipper.country_code,
                StateProvinceCode=payload.shipper.state_code
            ),
            AttentionName=payload.shipper.person_name,
        ),
        ShipTo=ShipToType(
            Name=payload.recipient.company_name,
            Address=AddressType(
                AddressLine=payload.recipient.address_lines,
                City=payload.recipient.city,
                PostalCode=payload.recipient.postal_code,
                CountryCode=payload.recipient.country_code,
                StateProvinceCode=payload.recipient.state_code
            ),
            AttentionName=payload.recipient.person_name,
        ),
        PaymentInformation=PaymentInformationType(
            Payer=PayerType(
                Name=payload.shipment.payment_country_code
                or payload.shipper.country_code,
                Address=AddressType(
                    City=payload.shipper.city,
                    PostalCode=payload.shipper.postal_code,
                    CountryCode=payload.shipper.country_code,
                    AddressLine=payload.shipper.address_lines,
                ),
                ShipperNumber=payload.shipper.account_number
                or payload.shipment.payment_account_number,
            ),
            ShipmentBillingOption=RateCodeDescriptionType(Code=10),
        ),
        Service=RateCodeDescriptionType(Code=service.value, Description=None),
        HandlingUnitOne=HandlingUnitType(
            Quantity=1, Type=RateCodeDescriptionType(Code="SKD")
        ),
        ShipmentServiceOptions=ShipmentServiceOptionsType(
            PickupOptions=PickupOptionsType(WeekendPickupIndicator="")
        ),
        DensityEligibleIndicator="",
        AdjustedWeightIndicator="",
        HandlingUnitWeight=HandlingUnitWeightType(
            Value=1,
            UnitOfMeasurement=UnitOfMeasurementType(
                Code=WeightUnit[payload.shipment.weight_unit].value
            ),
        ),
        PickupRequest=None,
        GFPOptions=OnCallInformationType(),
        TimeInTransitIndicator="",
        Commodity=[
            CommodityType(
                Description=c.description or "...",
                Weight=WeightType(
                    UnitOfMeasurement=UnitOfMeasurementType(
                        Code=WeightUnit[payload.shipment.weight_unit].value
                    ),
                    Value=c.weight,
                ),
                Dimensions=DimensionsType(
                    UnitOfMeasurement=UnitOfMeasurementType(
                        Code=DimensionUnit[payload.shipment.dimension_unit].value
                    ),
                    Width=c.width,
                    Height=c.height,
                    Length=c.length,
                ),
                NumberOfPieces=len(payload.shipment.items),
                PackagingType=RateCodeDescriptionType(
                    Code=PackagingType[c.packaging_type or "BOX"].value,
                    Description=None,
                ),
                FreightClass=50,
            )
            for c in payload.shipment.items
        ],
    )
    return Serializable(request, lambda _: partial(_request_serializer, settings=settings)(_))


def _request_serializer(request: FreightRateRequest, settings: Settings) -> str:
    namespace_ = """
                    xmlns:tns="http://schemas.xmlsoap.org/soap/envelope/" 
                    xmlns:common="http://www.ups.com/XMLSchema/XOLTWS/Common/v1.0" 
                    xmlns:upss="http://www.ups.com/XMLSchema/XOLTWS/UPSS/v1.0" 
                    xmlns:wsf="http://www.ups.com/schema/wsf" 
                    xmlns:xsd="http://www.w3.org/2001/XMLSchema" 
                    xmlns:frt="http://www.ups.com/XMLSchema/XOLTWS/FreightRate/v1.0"
                """.replace(" ", "").replace("\n", " ")
    return clean_namespaces(
        export(
            create_envelope(
                header_content=settings.Security,
                body_content=request
            ),
            namespacedef_=namespace_,
        ),
        envelope_prefix="tns:",
        header_child_prefix="upss:",
        header_child_name="UPSSecurity",
        body_child_name="FreightRateRequest",
        body_child_prefix="frt:",
    ).replace("common:Code", "rate:Code")
