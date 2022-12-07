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

import time
import typing
import karrio.lib as lib
import karrio.core.units as units
import karrio.core.models as models
import karrio.core.errors as errors
import karrio.providers.dhl_express.error as provider_error
import karrio.providers.dhl_express.units as provider_units
import karrio.providers.dhl_express.utils as provider_utils


def parse_rate_response(
    response: lib.Element, settings: provider_utils.Settings
) -> typing.Tuple[typing.List[models.RateDetails], typing.List[models.Message]]:
    quotes = lib.find_element("QtdShp", response, ResponseQtdShpType)
    rates: typing.List[models.RateDetails] = [
        _extract_quote(quote, settings)
        for quote in quotes
        if (quote.ShippingCharge is not None) or (quote.ShippingCharge is not None)
    ]

    return rates, provider_error.parse_error_response(response, settings)


def _extract_quote(
    quote: ResponseQtdShpType,
    settings: provider_utils.Settings,
) -> models.RateDetails:
    service = provider_units.ProductCode.map(quote.GlobalProductCode)
    charges = [
        ("Base charge", quote.WeightCharge),
        *((s.LocalServiceTypeName, s.ChargeValue) for s in quote.QtdShpExChrg),
    ]

    delivery_date = lib.to_date(quote.DeliveryDate[0].DlvyDateTime, "%Y-%m-%d %H:%M:%S")
    pricing_date = lib.to_date(quote.PricingDate)
    transit = (
        (delivery_date.date() - pricing_date.date()).days
        if all([delivery_date, pricing_date])
        else None
    )

    return models.RateDetails(
        carrier_name=settings.carrier_name,
        carrier_id=settings.carrier_id,
        currency=quote.CurrencyCode,
        transit_days=transit,
        service=service.name_or_key,
        total_charge=lib.to_decimal(quote.ShippingCharge),
        extra_charges=[
            models.ChargeDetails(
                name=name,
                amount=lib.to_decimal(amount),
                currency=quote.CurrencyCode,
            )
            for name, amount in charges
            if amount
        ],
        meta=dict(service_name=(service.name or quote.ProductShortName)),
    )


def rate_request(
    payload: models.RateRequest, settings: provider_utils.Settings
) -> lib.Serializable[DCTRequest]:
    packages = lib.to_packages(
        payload.parcels,
        provider_units.PackagePresets,
        required=["weight"],
        package_option_type=provider_units.ShippingOption,
    )
    is_international = payload.shipper.country_code != payload.recipient.country_code

    if any(settings.account_country_code or "") and (
        payload.shipper.country_code != settings.account_country_code
    ):
        raise errors.OriginNotServicedError(payload.shipper.country_code)
    if not is_international and payload.shipper.country_code in ["CA"]:
        raise errors.DestinationNotServicedError(payload.shipper.country_code)

    is_document = all([parcel.is_document for parcel in payload.parcels])
    is_dutiable = not is_document  # parcel and not document only so it is dutiable.
    products = lib.to_services(
        payload.services,
        is_document=is_document,
        is_international=is_international,
        is_envelope=("envelope" in (packages.package_type or "")),
        initializer=provider_units.shipping_services_initializer,
    )
    options = lib.to_shipping_options(
        payload.options,
        is_international=is_international,
        is_dutiable=is_dutiable,
        package_options=packages.options,
        initializer=provider_units.shipping_options_initializer,
    )

    weight_unit, dim_unit = (
        provider_units.COUNTRY_PREFERED_UNITS.get(payload.shipper.country_code)
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
                NetworkTypeCode=provider_units.NetworkType.both_time_and_day_definite.value,
                WeightUnit=weight_unit.value,
                DimensionUnit=dim_unit.value,
                ReadyTime=time.strftime("PT%HH%MM"),
                Date=time.strftime("%Y-%m-%d"),
                IsDutiable=("Y" if is_dutiable else "N"),
                Pieces=PiecesType(
                    Piece=[
                        PieceType(
                            PieceID=package.parcel.id or f"{index}",
                            PackageTypeCode=provider_units.DCTPackageType.map(
                                package.packaging_type or "your_packaging"
                            ).value,
                            Depth=package.length.map(provider_units.MeasurementOptions)[
                                dim_unit.name
                            ],
                            Width=package.width.map(provider_units.MeasurementOptions)[
                                dim_unit.name
                            ],
                            Height=package.height.map(
                                provider_units.MeasurementOptions
                            )[dim_unit.name],
                            Weight=package.weight[weight_unit.name],
                        )
                        for index, package in enumerate(packages, 1)
                    ]
                ),
                NumberOfPieces=len(packages),
                ShipmentWeight=packages.weight[weight_unit.name],
                Volume=None,
                PaymentAccountNumber=settings.account_number,
                InsuredCurrency=(
                    options.currency.state
                    if options.dhl_shipment_insurance.state
                    else None
                ),
                InsuredValue=options.dhl_shipment_insurance.state,
                PaymentType=None,
                AcctPickupCloseTime=None,
                QtdShp=[
                    QtdShpType(
                        GlobalProductCode=product.value,
                        LocalProductCode=product.value,
                        QtdShpExChrg=[
                            QtdShpExChrgType(SpecialServiceType=option.code)
                            for _, option in options.items()
                        ],
                    )
                    for product in products
                ],
            ),
            Dutiable=(
                DCTDutiable(
                    DeclaredValue=(options.declared_value.state or 1.0),
                    DeclaredCurrency=(
                        options.currency.state
                        or units.CountryCurrency[
                            payload.shipper.country_code
                        ].value
                    ),
                )
                if is_dutiable
                else None
            ),
        ),
    )

    return lib.Serializable(request, _request_serializer)


def _request_serializer(request: DCTRequest) -> str:
    namespacedef_ = (
        'xmlns:p="http://www.dhl.com" '
        'xmlns:p1="http://www.dhl.com/datatypes" '
        'xmlns:p2="http://www.dhl.com/DCTRequestdatatypes" '
        'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" '
        'xsi:schemaLocation="http://www.dhl.com DCT-req.xsd "'
    )
    return lib.to_xml(
        request,
        name_="p:DCTRequest",
        namespacedef_=namespacedef_,
    ).replace('schemaVersion="2"', 'schemaVersion="2.0"')
