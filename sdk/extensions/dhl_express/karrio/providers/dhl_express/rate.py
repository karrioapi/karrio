import time
from functools import reduce
from typing import List, Tuple, cast, Iterable
from dhl_express_lib.dct_req_global_2_0 import (
    DCTRequest,
    DCTTo,
    DCTFrom,
    GetQuoteType,
    BkgDetailsType,
    PiecesType,
    MetaData,
    PieceType,
    QtdShpType,
    QtdShpExChrgType,
)
from dhl_express_lib.dct_requestdatatypes_global import DCTDutiable
from dhl_express_lib.dct_response_global_2_0 import QtdShpType as ResponseQtdShpType

from karrio.core.errors import DestinationNotServicedError, OriginNotServicedError
from karrio.core.utils import Serializable, Element, NF, XP, DF
from karrio.core.units import Packages, Options, Package, Services, CountryCurrency
from karrio.core.models import RateDetails, Message, ChargeDetails, RateRequest
from karrio.providers.dhl_express.units import (
    ProductCode,
    DCTPackageType,
    PackagePresets,
    ShippingOption,
    NetworkType,
    COUNTRY_PREFERED_UNITS,
    MeasurementOptions,
)
from karrio.providers.dhl_express.utils import Settings
from karrio.providers.dhl_express.error import parse_error_response


def parse_rate_response(
    response: Element, settings: Settings
) -> Tuple[List[RateDetails], List[Message]]:
    quotes = XP.find("QtdShp", response, ResponseQtdShpType)
    rates: List[RateDetails] = [
        _extract_quote(quote, settings)
        for quote in quotes
        if (quote.ShippingCharge is not None) or (quote.ShippingCharge is not None)
    ]

    return rates, parse_error_response(response, settings)


def _extract_quote(quote: ResponseQtdShpType, settings: Settings) -> RateDetails:
    service = ProductCode.map(quote.GlobalProductCode)
    charges = [
        ("Base charge", quote.WeightCharge),
        *((s.LocalServiceTypeName, s.ChargeValue) for s in quote.QtdShpExChrg),
    ]

    delivery_date = DF.date(quote.DeliveryDate[0].DlvyDateTime, "%Y-%m-%d %H:%M:%S")
    pricing_date = DF.date(quote.PricingDate)
    transit = (
        (delivery_date.date() - pricing_date.date()).days
        if all([delivery_date, pricing_date])
        else None
    )

    return RateDetails(
        carrier_name=settings.carrier_name,
        carrier_id=settings.carrier_id,
        currency=quote.CurrencyCode,
        transit_days=transit,
        service=service.name_or_key,
        total_charge=NF.decimal(quote.ShippingCharge),
        extra_charges=[
            ChargeDetails(
                name=name,
                amount=NF.decimal(amount),
                currency=quote.CurrencyCode,
            )
            for name, amount in charges
            if amount
        ],
        meta=dict(service_name=(service.name or quote.ProductShortName)),
    )


def rate_request(payload: RateRequest, settings: Settings) -> Serializable[DCTRequest]:
    packages = Packages(
        payload.parcels,
        PackagePresets,
        required=["weight"],
        package_option_type=ShippingOption,
    )
    is_international = payload.shipper.country_code != payload.recipient.country_code

    if any(settings.account_country_code or "") and (
        payload.shipper.country_code != settings.account_country_code
    ):
        raise OriginNotServicedError(payload.shipper.country_code)
    if not is_international and payload.shipper.country_code in ["CA"]:
        raise DestinationNotServicedError(payload.shipper.country_code)

    is_document = all([parcel.is_document for parcel in payload.parcels])
    is_dutiable = not is_document  # parcel and not document only so it is dutiable.
    products = Services(
        ProductCode.apply_defaults(
            payload.services,
            is_international=is_international,
            is_document=is_document,
            is_envelope=("envelope" in (packages.package_type or "")),
        ),
        ProductCode,
    )
    options = ShippingOption.to_options(
        payload.options,
        is_international=is_international,
        is_dutiable=is_dutiable,
        package_options=packages.options,
    )

    weight_unit, dim_unit = (
        COUNTRY_PREFERED_UNITS.get(payload.shipper.country_code)
        or packages.compatible_units
    )

    request = DCTRequest(
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
                NetworkTypeCode=NetworkType.both_time_and_day_definite.value,
                WeightUnit=weight_unit.value,
                DimensionUnit=dim_unit.value,
                ReadyTime=time.strftime("PT%HH%MM"),
                Date=time.strftime("%Y-%m-%d"),
                IsDutiable=("Y" if is_dutiable else "N"),
                Pieces=PiecesType(
                    Piece=[
                        PieceType(
                            PieceID=package.parcel.id or f"{index}",
                            PackageTypeCode=DCTPackageType[
                                package.packaging_type or "your_packaging"
                            ].value,
                            Depth=package.length.map(MeasurementOptions)[dim_unit.name],
                            Width=package.width.map(MeasurementOptions)[dim_unit.name],
                            Height=package.height.map(MeasurementOptions)[
                                dim_unit.name
                            ],
                            Weight=package.weight[weight_unit.name],
                        )
                        for index, package in enumerate(
                            cast(Iterable[Package], packages), 1
                        )
                    ]
                ),
                NumberOfPieces=len(packages),
                ShipmentWeight=packages.weight[weight_unit.name],
                Volume=None,
                PaymentAccountNumber=settings.account_number,
                InsuredCurrency=(
                    options.currency if options.dhl_shipment_insurance else None
                ),
                InsuredValue=(
                    options.dhl_shipment_insurance.value
                    if options.dhl_shipment_insurance
                    else None
                ),
                PaymentType=None,
                AcctPickupCloseTime=None,
                QtdShp=[
                    QtdShpType(
                        GlobalProductCode=product.value,
                        LocalProductCode=product.value,
                        QtdShpExChrg=[
                            QtdShpExChrgType(SpecialServiceType=code)
                            for _, code, _ in options.as_list()
                        ],
                    )
                    for product in products
                ],
            ),
            Dutiable=(
                DCTDutiable(
                    DeclaredValue=(options.declared_value or 1.0),
                    DeclaredCurrency=(
                        options.currency
                        or CountryCurrency[payload.shipper.country_code].value
                    ),
                )
                if is_dutiable
                else None
            ),
        ),
    )

    return Serializable(request, _request_serializer)


def _request_serializer(request: DCTRequest) -> str:
    namespacedef_ = (
        'xmlns:p="http://www.dhl.com" '
        'xmlns:p1="http://www.dhl.com/datatypes" '
        'xmlns:p2="http://www.dhl.com/DCTRequestdatatypes" '
        'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" '
        'xsi:schemaLocation="http://www.dhl.com DCT-req.xsd "'
    )
    return XP.export(
        request,
        name_="p:DCTRequest",
        namespacedef_=namespacedef_,
    ).replace('schemaVersion="2"', 'schemaVersion="2.0"')
