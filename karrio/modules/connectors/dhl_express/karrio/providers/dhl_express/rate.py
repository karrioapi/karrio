import karrio.schemas.dhl_express.dct_requestdatatypes_global as dhl_global
import karrio.schemas.dhl_express.dct_response_global_3_0 as dhl_response
import karrio.schemas.dhl_express.dct_req_global_3_0 as dhl
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
    _response: lib.Deserializable[lib.Element],
    settings: provider_utils.Settings,
) -> typing.Tuple[typing.List[models.RateDetails], typing.List[models.Message]]:
    response = _response.deserialize()

    messages = provider_error.parse_error_response(response, settings)
    quotes: typing.List[dhl_response.QtdShpType] = lib.find_element(
        "QtdShp", response, dhl_response.QtdShpType
    )
    rates: typing.List[models.RateDetails] = [
        _extract_quote(quote, settings, _response.ctx)
        for quote in quotes
        if (
            quote.ShippingCharge is not None
            and lib.to_decimal(quote.ShippingCharge) > 0
        )
    ]

    return [_ for _ in rates if _ is not None], messages


def _extract_quote(
    quote: dhl_response.QtdShpType,
    settings: provider_utils.Settings,
    ctx: typing.Dict[str, typing.Any] = {},
) -> models.RateDetails:
    is_document = ctx.get("is_document", False)
    service = provider_units.ShippingService.map(quote.GlobalProductCode)

    # Filter out services that are not specific to package content
    if settings.connection_config.skip_service_filter.state != True and (
        is_document is False and " DOC" in quote.LocalProductCode
    ):
        return None

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
        meta=dict(service_name=f"DHL {quote.LocalProductName}"),
    )


def rate_request(
    payload: models.RateRequest, settings: provider_utils.Settings
) -> lib.Serializable:
    packages = lib.to_packages(
        payload.parcels,
        provider_units.PackagePresets,
        required=["weight"],
        package_option_type=provider_units.ShippingOption,
    )
    is_international = payload.shipper.country_code != payload.recipient.country_code

    is_document = all([parcel.is_document for parcel in payload.parcels])
    is_from_EU = payload.shipper.country_code in units.EUCountry
    is_to_EU = payload.recipient.country_code in units.EUCountry
    is_dutiable = is_international and not is_document and not (is_from_EU and is_to_EU)

    services = lib.to_services(
        payload.services,
        is_document=is_document,
        is_international=is_international,
        origin_country=payload.shipper.country_code,
        is_envelope=("envelope" in (packages.package_type or "")),
        initializer=provider_units.shipping_services_initializer,
    )
    options = lib.to_shipping_options(
        payload.options,
        package_options=packages.options,
        origin_country=payload.shipper.country_code,
        initializer=provider_units.shipping_options_initializer,
    )
    option_items = [
        option for _, option in options.items() if option.state is not False
    ]
    weight_unit, dim_unit = (
        provider_units.COUNTRY_PREFERED_UNITS.get(payload.shipper.country_code)
        or packages.compatible_units
    )
    currency = (
        options.currency.state
        or units.CountryCurrency[payload.shipper.country_code].value
    )

    request = dhl.DCTRequest(
        GetQuote=dhl.GetQuoteType(
            Request=settings.Request(
                MetaData=dhl.MetaData(SoftwareName="3PV", SoftwareVersion=1.0)
            ),
            From=dhl.DCTFrom(
                CountryCode=payload.shipper.country_code,
                Postalcode=payload.shipper.postal_code,
                City=payload.shipper.city,
            ),
            To=dhl.DCTTo(
                CountryCode=payload.recipient.country_code,
                Postalcode=payload.recipient.postal_code,
                City=payload.recipient.city,
            ),
            BkgDetails=dhl.BkgDetailsType(
                PaymentCountryCode=payload.shipper.country_code,
                NetworkTypeCode=provider_units.NetworkType.both_time_and_day_definite.value,
                WeightUnit=weight_unit.value,
                DimensionUnit=dim_unit.value,
                ReadyTime=time.strftime("PT%HH%MM"),
                Date=time.strftime("%Y-%m-%d"),
                IsDutiable=("Y" if is_dutiable else "N"),
                Pieces=dhl.PiecesType(
                    Piece=[
                        dhl.PieceType(
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
                PaymentAccountNumber=lib.text(settings.account_number),
                InsuredCurrency=(
                    currency if options.dhl_shipment_insurance.state else None
                ),
                InsuredValue=options.dhl_shipment_insurance.state,
                PaymentType=None,
                AcctPickupCloseTime=None,
                QtdShp=(
                    [
                        dhl.QtdShpType(
                            GlobalProductCode=svc.value,
                            LocalProductCode=svc.value,
                            QtdShpExChrg=(
                                [
                                    dhl.QtdShpExChrgType(SpecialServiceType=option.code)
                                    for option in option_items
                                ]
                                if any(option_items)
                                else None
                            ),
                        )
                        for svc in services
                    ]
                    if any([_.value for _ in services])
                    else None
                ),
            ),
            Dutiable=(
                dhl_global.DCTDutiable(
                    DeclaredValue=(options.declared_value.state or 1.0),
                    DeclaredCurrency=currency,
                )
                if is_dutiable
                else None
            ),
        ),
    )

    return lib.Serializable(
        request,
        _request_serializer,
        dict(is_international=is_international, is_document=is_document),
    )


def _request_serializer(request: dhl.DCTRequest) -> str:
    namespacedef_ = (
        'xmlns:p="http://www.dhl.com" '
        'xmlns:p1="http://www.dhl.com/datatypes" '
        'xmlns:p2="http://www.dhl.com/DCTRequestdatatypes" '
        'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" '
        'xsi:schemaLocation="http://www.dhl.com DCT-req.xsd"'
    )
    return lib.to_xml(
        request,
        name_="p:DCTRequest",
        namespacedef_=namespacedef_,
    ).replace('schemaVersion="3"', 'schemaVersion="3.0"')
