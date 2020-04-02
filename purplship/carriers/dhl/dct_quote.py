import time
from datetime import datetime
from functools import reduce
from typing import List, Tuple
from pydhl.dct_req_global_2_0 import (
    DCTRequest,
    DCTTo,
    DCTFrom,
    GetQuoteType,
    BkgDetailsType,
    PiecesType,
    MetaData,
    PieceType,
    QtdShpType,
)
from pydhl.dct_response_global_2_0 import QtdShpType as ResponseQtdShpType
from purplship.core.utils import export, Serializable, Element, format_date, decimal
from purplship.core.errors import RequiredFieldError
from purplship.core.units import Package
from purplship.core.models import RateDetails, Message, ChargeDetails, RateRequest
from purplship.carriers.dhl.units import (
    Product,
    ProductCode,
    DCTPackageType,
    Dimension,
    WeightUnit,
    PackagePresets,
)
from purplship.carriers.dhl.utils import Settings
from purplship.carriers.dhl.error import parse_error_response


def parse_dct_response(
    response: Element, settings: Settings
) -> Tuple[List[RateDetails], List[Message]]:
    qtdshp_list = response.xpath(".//*[local-name() = $name]", name="QtdShp")
    quotes: List[RateDetails] = [
        _extract_quote(qtdshp_node, settings) for qtdshp_node in qtdshp_list
    ]
    return quotes, parse_error_response(response, settings)


def _extract_quote(qtdshp_node: Element, settings: Settings) -> RateDetails:
    qtdshp = ResponseQtdShpType()
    qtdshp.build(qtdshp_node)
    ExtraCharges = list(
        map(
            lambda s: ChargeDetails(
                name=s.LocalServiceTypeName, amount=decimal(s.ChargeValue or 0)
            ),
            qtdshp.QtdShpExChrg,
        )
    )
    Discount_ = reduce(
        lambda d, ec: d + ec.amount if "Discount" in ec.name else d, ExtraCharges, 0.0
    )
    DutiesAndTaxes_ = reduce(
        lambda d, ec: d + ec.amount if "TAXES PAID" in ec.name else d, ExtraCharges, 0.0
    )
    DlvyDateTime = qtdshp.DeliveryDate[0].DlvyDateTime
    delivery_date = (
        datetime.strptime(str(DlvyDateTime), "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d")
        if DlvyDateTime is not None
        else None
    )
    service_name = next(
        (p.name for p in Product if p.value in qtdshp.LocalProductName),
        qtdshp.LocalProductName,
    )
    return RateDetails(
        carrier=settings.carrier,
        carrier_name=settings.carrier_name,
        currency=qtdshp.CurrencyCode,
        estimated_delivery=format_date(delivery_date),
        service=service_name,
        base_charge=decimal(qtdshp.WeightCharge or 0),
        total_charge=decimal(qtdshp.ShippingCharge or 0),
        duties_and_taxes=decimal(DutiesAndTaxes_),
        discount=decimal(Discount_),
        extra_charges=list(
            map(
                lambda s: ChargeDetails(
                    name=s.LocalServiceTypeName, amount=decimal(s.ChargeValue or 0)
                ),
                qtdshp.QtdShpExChrg,
            )
        ),
    )


def dct_request(payload: RateRequest, settings: Settings) -> Serializable[DCTRequest]:
    parcel_preset = (
        PackagePresets[payload.parcel.package_preset].value
        if payload.parcel.package_preset
        else None
    )
    package = Package(payload.parcel, parcel_preset)

    if package.weight.value is None:
        raise RequiredFieldError("parcel.weight")

    products = [
        ProductCode[svc].value
        for svc in payload.services
        if svc in ProductCode.__members__
    ]

    request = DCTRequest(
        schemaVersion=2.0,
        GetQuote=GetQuoteType(
            Request=settings.Request(
                MetaData=MetaData(SoftwareName="3PV", SoftwareVersion=1.0)
            ),
            From=DCTFrom(
                CountryCode=payload.shipper.country_code,
                Postalcode=payload.shipper.postal_code,
                City=payload.shipper.city,
                Suburb=payload.shipper.state_code,
            ),
            To=DCTTo(
                CountryCode=payload.recipient.country_code,
                Postalcode=payload.recipient.postal_code,
                City=payload.recipient.city,
                Suburb=payload.recipient.state_code,
            ),
            BkgDetails=BkgDetailsType(
                PaymentCountryCode=payload.shipper.country_code,
                NetworkTypeCode=None,
                WeightUnit=WeightUnit[package.weight_unit.name].value,
                DimensionUnit=Dimension[package.dimension_unit.name].value,
                ReadyTime=time.strftime("PT%HH%MM"),
                Date=time.strftime("%Y-%m-%d"),
                IsDutiable=("N" if payload.parcel.is_document else "Y"),
                Pieces=PiecesType(
                    Piece=[
                        PieceType(
                            PieceID=payload.parcel.id,
                            PackageTypeCode=DCTPackageType[
                                package.packaging_type or "your_packaging"
                            ].value,
                            Depth=package.length.value,
                            Width=package.width.value,
                            Height=package.height.value,
                            Weight=package.weight.value,
                        )
                    ]
                ),
                NumberOfPieces=1,
                ShipmentWeight=package.weight.value,
                Volume=None,
                PaymentAccountNumber=None,
                InsuredCurrency=None,
                InsuredValue=None,
                PaymentType=None,
                AcctPickupCloseTime=None,
                QtdShp=[
                    QtdShpType(
                        GlobalProductCode=product,
                        LocalProductCode=product,
                        QtdShpExChrg=None,
                    )
                    for product in products
                ],
            ),
            Dutiable=None,
        ),
    )
    return Serializable(request, _request_serializer)


def _request_serializer(request: DCTRequest) -> str:
    return export(
        request,
        name_="p:DCTRequest",
        namespacedef_='xmlns:p="http://www.dhl.com" xmlns:p1="http://www.dhl.com/datatypes" xmlns:p2="http://www.dhl.com/DCTRequestdatatypes" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.dhl.com DCT-req.xsd "',
    )
