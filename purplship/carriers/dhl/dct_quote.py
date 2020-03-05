import time
from datetime import datetime
from functools import reduce
from typing import List, Tuple
from pydhl.dct_req_global_2_0 import (
    DCTRequest, DCTTo, DCTFrom, GetQuoteType, BkgDetailsType, PiecesType, MetaData,
    PieceType, QtdShpType, QtdShpExChrgType, DCTDutiable
)
from pydhl.dct_response_global_2_0 import QtdShpType as ResponseQtdShpType
from purplship.core.utils.helpers import export
from purplship.core.utils.serializable import Serializable
from purplship.core.utils.xml import Element
from purplship.core.units import DimensionUnit, WeightUnit, Currency
from purplship.core.models import (
    RateDetails, Error, ChargeDetails, RateRequest
)
from purplship.carriers.dhl.units import Product, Service, DCTPackageType
from purplship.carriers.dhl.utils import Settings
from purplship.carriers.dhl.error import parse_error_response


def parse_dct_response(response: Element, settings: Settings) -> Tuple[List[RateDetails], List[Error]]:
    qtdshp_list = response.xpath(".//*[local-name() = $name]", name="QtdShp")
    quotes: List[RateDetails] = [_extract_quote(qtdshp_node, settings) for qtdshp_node in qtdshp_list]
    return quotes, parse_error_response(response, settings)


def _extract_quote(qtdshp_node: Element, settings: Settings) -> RateDetails:
    qtdshp = ResponseQtdShpType()
    qtdshp.build(qtdshp_node)
    ExtraCharges = list(
        map(
            lambda s: ChargeDetails(name=s.LocalServiceTypeName, amount=float(s.ChargeValue or 0)),
            qtdshp.QtdShpExChrg,
        )
    )
    Discount_ = reduce(
        lambda d, ec: d + ec.amount if "Discount" in ec.name else d,
        ExtraCharges,
        0.0,
    )
    DutiesAndTaxes_ = reduce(
        lambda d, ec: d + ec.amount if "TAXES PAID" in ec.name else d,
        ExtraCharges,
        0.0,
    )
    delivery_ = str(qtdshp.DeliveryDate[0].DlvyDateTime)
    return RateDetails(
        carrier=settings.carrier_name,
        currency=qtdshp.CurrencyCode,
        delivery_date=datetime.strptime(
            delivery_,
            "%Y-%m-%d %H:%M:%S"
        ).strftime("%Y-%m-%d") if delivery_ else None,
        service_name=qtdshp.LocalProductName,
        service_type=qtdshp.NetworkTypeCode,
        base_charge=float(qtdshp.WeightCharge or 0),
        total_charge=float(qtdshp.ShippingCharge or 0),
        duties_and_taxes=DutiesAndTaxes_,
        discount=Discount_,
        extra_charges=list(
            map(
                lambda s: ChargeDetails(
                    name=s.LocalServiceTypeName,
                    amount=float(s.ChargeValue or 0),
                ),
                qtdshp.QtdShpExChrg,
            )
        ),
    )


def dct_request(payload: RateRequest, settings: Settings) -> Serializable[DCTRequest]:
    default_product_code = (
        Product.EXPRESS_WORLDWIDE_DOC
        if payload.shipment.is_document
        else Product.EXPRESS_WORLDWIDE
    )
    products = [
        Product[svc]
        for svc in payload.shipment.services
        if svc in Product.__members__
    ] + [default_product_code]
    is_dutiable = not payload.shipment.declared_value
    default_packaging_type = (
        DCTPackageType.SM if payload.shipment.is_document else DCTPackageType.BOX
    )
    option_codes = [code for code in payload.shipment.options.keys()]
    options = (
        [Service[code] for code in option_codes if code in Service.__members__] +
        (
            []
            if not payload.shipment.insured_amount
            or "Shipment_Insurance" in option_codes
            else [Service.Shipment_Insurance]
        ) +
        (
            []
            if not is_dutiable
            or "Duties_and_Taxes_Paid" in option_codes
            else [Service.Duties_and_Taxes_Paid]
        )
    )

    request = DCTRequest(
        schemaVersion="1.0",
        GetQuote=GetQuoteType(
            Request=settings.Request(MetaData=MetaData(SoftwareName="3PV", SoftwareVersion="1.0")),
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
                PaymentCountryCode=payload.shipment.payment_country_code or "CA",
                NetworkTypeCode=None,
                WeightUnit=WeightUnit[payload.shipment.weight_unit or "KG"].value,
                DimensionUnit=DimensionUnit[
                    payload.shipment.dimension_unit or "CM"
                ].value,
                ReadyTime=time.strftime("PT%HH%MM"),
                Date=time.strftime("%Y-%m-%d"),
                IsDutiable="Y" if is_dutiable else "N",
                Pieces=PiecesType(
                    Piece=[
                        PieceType(
                            PieceID=piece.id or str(index),
                            PackageTypeCode=(
                                DCTPackageType[piece.packaging_type]
                                if not piece.packaging_type
                                else default_packaging_type
                            ).value,
                            Height=piece.height,
                            Width=piece.width,
                            Weight=piece.weight,
                            Depth=piece.length,
                        )
                        for index, piece in enumerate(payload.shipment.items)
                    ]
                ),
                NumberOfPieces=payload.shipment.total_items,
                ShipmentWeight=payload.shipment.total_weight,
                Volume=None,
                PaymentAccountNumber=payload.shipment.payment_account_number,
                InsuredCurrency=(
                    (payload.shipment.currency or Currency.USD.name)
                    if Service.Shipment_Insurance in options else None
                ),
                InsuredValue=payload.shipment.insured_amount,
                PaymentType=payload.shipment.payment_type,
                AcctPickupCloseTime=None,
                QtdShp=[
                    QtdShpType(
                        GlobalProductCode=product.value,
                        LocalProductCode=product.value,
                        QtdShpExChrg=[
                            QtdShpExChrgType(
                                SpecialServiceType=svc.value,
                                LocalSpecialServiceType=None,
                            )
                            for svc in options
                        ]
                        if len(options) > 0 else None,
                    )
                    for product in products
                ],
            ),
            Dutiable=(
                DCTDutiable(
                    DeclaredCurrency=payload.shipment.currency or Currency.USD.name,
                    DeclaredValue=payload.shipment.declared_value or 0,
                )
                if is_dutiable else None
            ),
        )
    )
    return Serializable(request, _request_serializer)


def _request_serializer(request: DCTRequest) -> str:
    return export(
        request,
        name_="p:DCTRequest",
        namespacedef_='xmlns:p="http://www.dhl.com" xmlns:p1="http://www.dhl.com/datatypes" xmlns:p2="http://www.dhl.com/DCTRequestdatatypes" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.dhl.com DCT-req.xsd "',
    ).replace('schemaVersion="1."', 'schemaVersion="1.0"')
