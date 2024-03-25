import functools
import karrio.schemas.tnt.rating_request as tnt
import karrio.schemas.tnt.rating_response as rating
import typing
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.tnt.error as provider_error
import karrio.providers.tnt.units as provider_units
import karrio.providers.tnt.utils as provider_utils


def parse_rate_response(
    _response: lib.Deserializable[lib.Element],
    settings: provider_utils.Settings,
) -> typing.Tuple[typing.List[models.RateDetails], typing.List[models.Message]]:
    response = _response.deserialize()

    messages = provider_error.parse_error_response(response, settings)
    services: typing.List[rating.ratedServices] = lib.find_element(
        "ratedServices", response, rating.ratedServices
    )
    rates: typing.List[models.RateDetails] = sum(
        [
            [
                _extract_details((rate, svc.currency), settings)
                for rate in svc.ratedService
            ]
            for svc in services
        ],
        start=[],
    )

    return rates, messages


def _extract_details(
    details: typing.Tuple[rating.ratedService, str],
    settings: provider_utils.Settings,
) -> models.RateDetails:
    rate, currency = details
    service = provider_units.ShippingService.map(rate.product.id)
    charges = [
        ("Base charge", rate.totalPriceExclVat),
        ("VAT", rate.vatAmount),
        *(
            (charge.description, charge.chargeValue)
            for charge in rate.chargeElements.chargeElement
        ),
    ]

    return models.RateDetails(
        carrier_name=settings.carrier_name,
        carrier_id=settings.carrier_id,
        currency=currency,
        service=service.name_or_key,
        total_charge=lib.to_decimal(rate.totalPrice),
        extra_charges=[
            models.ChargeDetails(
                name=name,
                amount=lib.to_decimal(amount),
                currency=currency,
            )
            for name, amount in charges
            if amount is not None
        ],
        meta=dict(service_name=rate.product.productDesc),
    )


def rate_request(
    payload: models.RateRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    service = lib.to_services(payload.services, provider_units.ShippingService).first
    packages = lib.to_packages(
        payload.parcels,
        presets=provider_units.PackagePresets,
        package_option_type=provider_units.PackageType,
    )
    options = lib.to_shipping_options(
        payload.options,
        package_options=packages.options,
        shipper_country_code=payload.shipper.country_code,
        recipient_country_code=payload.recipient.country_code,
        is_international=(
            payload.shipper.country_code != payload.recipient.country_code
        ),
        initializer=provider_units.shipping_options_initializer,
    )
    is_document = all([parcel.is_document for parcel in payload.parcels])

    request = tnt.priceRequest(
        appId=settings.connection_config.app_id.state or "PC",
        appVersion="3.2",
        priceCheck=[
            tnt.priceCheck(
                rateId=None,
                sender=tnt.address(
                    country=payload.shipper.country_code,
                    town=payload.shipper.city,
                    postcode=payload.shipper.postal_code,
                ),
                delivery=tnt.address(
                    country=payload.recipient.country_code,
                    town=payload.recipient.city,
                    postcode=payload.recipient.postal_code,
                ),
                collectionDateTime=lib.fdatetime(
                    options.shipment_date.state,
                    current_format="%Y-%m-%d",
                    output_format="%Y-%m-%dT%H:%M:%S",
                ),
                product=tnt.product(
                    id=getattr(service, "value", None),
                    division=next(
                        (
                            option.code
                            for key, option in options.items()
                            if "division" in key and option.state is True
                        ),
                        None,
                    ),
                    productDesc=None,
                    type_=("D" if is_document else "N"),
                    options=(
                        tnt.options(
                            option=[
                                tnt.option(optionCode=option.code)
                                for key, option in options.items()
                                if "division" not in key
                            ]
                        )
                        if any(options.items())
                        else None
                    ),
                ),
                account=(
                    tnt.account(
                        accountNumber=settings.account_number,
                        accountCountry=settings.account_country_code,
                    )
                    if any([settings.account_number, settings.account_country_code])
                    else None
                ),
                insurance=(
                    tnt.insurance(
                        insuranceValue=options.insurance.state,
                        goodsValue=options.declared_value.state,
                    )
                    if options.insurance.state is not None
                    else None
                ),
                termsOfPayment=provider_units.PaymentType.sender.value,
                currency=options.currency.state,
                priceBreakDown=True,
                consignmentDetails=tnt.consignmentDetails(
                    totalWeight=packages.weight.KG,
                    totalVolume=packages.volume.m3,
                    totalNumberOfPieces=len(packages),
                ),
                pieceLine=[
                    tnt.pieceLine(
                        numberOfPieces=1,
                        pieceMeasurements=tnt.pieceMeasurements(
                            length=package.length.M,
                            width=package.width.M,
                            height=package.height.M,
                            weight=package.weight.KG,
                        ),
                        pallet=(package.packaging_type == "pallet"),
                    )
                    for package in packages
                ],
            )
        ],
    )

    return lib.Serializable(
        request,
        functools.partial(
            lib.to_xml,
            namespacedef_='xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"',
        ),
    )
