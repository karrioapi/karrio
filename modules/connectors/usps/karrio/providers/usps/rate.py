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
                    _
                    for _ in [
                        _extract_details(rate, settings, _response.ctx)
                        for rate in response["rateOptions"]
                    ]
                    if _ is not None
                ],
            )
            for _, response in enumerate(responses, start=1)
            if response.get("rateOptions") is not None
        ]
    )

    return rates, messages


def _extract_details(
    data: dict,
    settings: provider_utils.Settings,
    ctx: dict = dict(),
) -> typing.Optional[models.RateDetails]:
    details = lib.to_object(rating.RateOptionType, data)
    rate = details.rates[0]
    service = provider_units.ShippingService.map(rate.mailClass)
    price_type = ctx.get("price_type")
    rate_indicator = ctx.get("rate_indicator")
    charges = [
        *[(_.description, lib.to_money(_.price)) for _ in details.rates],
        *[
            (_.name, lib.to_money(_.price))
            for _ in details.extraServices
            if lib.to_money(_.price) > 0 and _.priceType == price_type
        ],
    ]

    # Skip rate if rate indicator or rate indicator exclusion matches
    skip = lib.identity(
        (rate_indicator is not None and rate_indicator != rate.rateIndicator)
        or (price_type != rate.priceType)
    )

    if skip:
        return None

    return models.RateDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        service=service.name_or_key,
        total_charge=lib.to_money(details.totalBasePrice),
        currency="USD",
        extra_charges=[
            models.ChargeDetails(name=name, currency="USD", amount=amount)
            for name, amount in charges
            if amount > 0
        ],
        meta=dict(
            service_name=service.name or rate.mailClass,
            usps_processing_category=rate.processingCategory,
            usps_zone=lib.failsafe(lambda: rate.zone),
            usps_rate_indicator=rate.rateIndicator,
            usps_price_type=rate.priceType,
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

    services = lib.to_services(payload.services, provider_units.ShippingService)
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
    rate_indicator = lib.identity(
        options.usps_rate_indicator.state
        or provider_units.PackagingType.map(packages.package_type).name
        or None
    )

    # map data to convert karrio model to usps specific type
    request = [
        usps.RateRequestType(
            originZIPCode=shipper.postal_code,
            destinationZIPCode=recipient.postal_code,
            weight=package.weight.LB,
            length=package.length.IN,
            width=package.width.IN,
            height=package.height.IN,
            # mailClass=None,
            mailClasses=[
                service.value
                for service in (
                    services
                    if any(services)
                    else [provider_units.ShippingService.usps_all]
                )
            ],
            priceType=price_type,
            mailingDate=lib.fdate(
                package.options.shipment_date.state or time.strftime("%Y-%m-%d")
            ),
            accountType=settings.account_type or "EPS",
            accountNumber=lib.identity(
                settings.account_number or settings.connection_config.mailer_id.state
            ),
            itemValue=lib.identity(
                package.items.value_amount if len(package.items) > 0 else None
            ),
            extraServices=[
                lib.to_int(_.code)
                for __, _ in options.items()
                if __ not in provider_units.CUSTOM_OPTIONS
            ],
        )
        for package in packages
    ]

    return lib.Serializable(
        request,
        lib.to_dict,
        dict(
            price_type=price_type,
            usps_rate_indicator=rate_indicator,
        ),
    )
