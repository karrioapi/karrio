"""Karrio USPS rating API implementation."""

import karrio.schemas.usps.rate_request as usps
import karrio.schemas.usps.rate_response as rating

import time
import typing
import karrio.lib as lib
import karrio.core.units as units
import karrio.core.models as models
import karrio.core.errors as errors
import karrio.providers.usps.error as error
import karrio.providers.usps.utils as provider_utils
import karrio.providers.usps.units as provider_units


def parse_rate_response(
    _response: lib.Deserializable[dict],
    settings: provider_utils.Settings,
) -> typing.Tuple[typing.List[models.RateDetails], typing.List[models.Message]]:
    responses = _response.deserialize()

    messages = error.parse_error_response(responses, settings)
    rates = lib.to_multi_piece_rates(
        [
            (
                f"{_}",
                [
                    _ for _ in [
                        _extract_details(dict(rate=rate, rateOption=rateOption), settings, _response.ctx)
                        for pricingOption in response.get("pricingOptions", [])
                        for shippingOption in pricingOption.get("shippingOptions", [])
                        for rateOption in shippingOption.get("rateOptions", [])
                        for rate in rateOption.get("rates", [])
                    ]
                    if _ is not None
                ],
            )
            for _, response in enumerate(responses, start=1)
        ]
    )

    return rates, messages


def _extract_details(
    data: dict,
    settings: provider_utils.Settings,
    ctx: dict = dict(),
) -> typing.Optional[models.RateDetails]:
    currency = "USD"
    machinable_piece = data.get("machinable_piece")
    rate = lib.to_object(rating.RateType, data['rate'])
    rateOption = lib.to_object(rating.RateOptionType, data['rateOption'])
    product_name = rate.productName or rate.description or rate.mailClass
    service_code = provider_units.ShippingService.to_product_code(product_name)
    service_name = provider_units.ShippingService.to_product_name(service_code)

    if machinable_piece is True and "machinable" not in service_code:
        return None
    if machinable_piece is False and "machinable" in service_code:
        return None

    transit_days = lib.to_int(next(iter(rateOption.commitment.name.split(" "))))
    estimated_delivery = rateOption.commitment.scheduleDeliveryDate
    charges = [
        ("Base Price", lib.to_money(rateOption.totalBasePrice)),
        *[(extra.name, lib.to_money(extra.price)) for extra in rateOption.extraServices],
    ]

    return models.RateDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        service=service_code,
        total_charge=lib.to_money(rateOption.totalPrice),
        currency=currency,
        extra_charges=[
            models.ChargeDetails(
                currency=currency,
                amount=amount,
                name=name,
            )
            for name, amount in charges
        ],
        estimated_delivery=estimated_delivery,
        transit_days=transit_days,
        meta=dict(
            service_name=service_name,
            usps_mail_class=rate.mailClass,
            usps_guaranteed_delivery=lib.failsafe(lambda: rateOption.commitment.guaranteedDelivery),
            usps_processing_category=lib.failsafe(lambda: rate.processingCategory),
            usps_dimensional_weight=lib.failsafe(lambda: rate.dimensionalWeight),
            usps_rate_indicator=lib.failsafe(lambda: rate.rateIndicator),
            usps_price_type=lib.failsafe(lambda: rate.priceType),
            usps_rate_sku=lib.failsafe(lambda: rate.SKU),
            usps_zone=lib.failsafe(lambda: rate.zone),
            rate_zone=lib.failsafe(lambda: rate.zone),
            usps_extra_services=lib.failsafe(
                lambda: [lib.to_int(_.extraService) for _ in rateOption.extraServices]
            ),
        ),
    )


def rate_request(
    payload: models.RateRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    shipper = lib.to_address(payload.shipper)
    recipient = lib.to_address(payload.recipient)

    if (
        shipper.country_code is not None
        and shipper.country_code != units.Country.US.name
    ):
        raise errors.OriginNotServicedError(shipper.country_code)

    if (
        recipient.country_code is not None
        and recipient.country_code != units.Country.US.name
    ):
        raise errors.DestinationNotServicedError(recipient.country_code)

    services = lib.to_services(
        [provider_units.ShippingService.to_mail_class(_).name_or_key for _ in payload.services],
        provider_units.ShippingService
    )
    options = lib.to_shipping_options(
        payload.options,
        initializer=provider_units.shipping_options_initializer,
    )
    packages = lib.to_packages(
        payload.parcels,
        options=options,
        package_option_type=provider_units.ShippingOption,
        shipping_options_initializer=provider_units.shipping_options_initializer,
    )
    price_type = lib.identity(
        options.usps_price_type.state
        or settings.connection_config.price_type.state
        or "RETAIL"
    )

    package_mail_class = lambda package: lib.identity(
        provider_units.ShippingService.to_mail_class(package.options.usps_mail_class.state).value
        if package.options.usps_mail_class.state
        else getattr(services.first, "value", "ALL")
    )
    package_options = lambda package: lib.identity(
        package.options
        if package_mail_class(package) not in provider_units.INCOMPATIBLE_SERVICES
        else {}
    )

    # map data to convert karrio model to usps specific type
    request = [
        usps.RateRequestType(
            pricingOptions=[
                usps.PricingOptionType(
                    priceType=price_type,
                    paymentAccount=usps.PaymentAccountType(
                        accountType=settings.account_type,
                        accountNumber=settings.account_number,
                    ),
                )
            ],
            originZIPCode=shipper.postal_code,
            destinationZIPCode=recipient.postal_code,
            destinationEntryFacilityType=lib.identity(
                options.usps_destination_entry_facility_type.state
                or "NONE"
            ),
            packageDescription=usps.PackageDescriptionType(
                weight=package.weight.LB,
                length=package.length.IN,
                height=package.height.IN,
                width=package.width.IN,
                girth=lib.identity(
                    package.girth.value if package.packaging_type == "tube" else None
                ),
                mailClass=package_mail_class(package),
                extraServices=[
                    lib.to_int(_.code)
                    for __, _ in package_options(package).items()
                    if __ not in provider_units.CUSTOM_OPTIONS
                ],
                packageValue=package.options.package_value.state,
                mailingDate=lib.fdate(
                    package.options.shipment_date.state or time.strftime("%Y-%m-%d")
                ),
            ),
            shippingFilter=package.options.usps_shipping_filter.state,
        )
        for package in packages
    ]

    return lib.Serializable(
        request,
        lib.to_dict,
        dict(
            price_type=price_type,
            machinable_piece=options.usps_machinable_piece.state,
        ),
    )
