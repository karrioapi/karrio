"""Karrio USPS rating API implementation."""

import karrio.schemas.usps_international.rate_request as usps
import karrio.schemas.usps_international.rate_response as rating

import time
import typing
import karrio.lib as lib
import karrio.core.units as units
import karrio.core.models as models
import karrio.core.errors as errors
import karrio.providers.usps_international.error as error
import karrio.providers.usps_international.utils as provider_utils
import karrio.providers.usps_international.units as provider_units


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
                [_extract_details(rate, settings) for rate in response["rateOptions"]],
            )
            for _, response in enumerate(responses, start=1)
            if response.get("rateOptions") is not None
        ]
    )

    return rates, messages


def _extract_details(
    data: dict,
    settings: provider_utils.Settings,
) -> models.RateDetails:
    rate = lib.to_object(rating.RateOptionType, data)
    mail_class = rate.rates[0].mailClass
    service = provider_units.ShippingService.map(mail_class)
    charges = [
        ("Base Charge", lib.to_money(rate.totalBasePrice)),
        *[(_.description, lib.to_money(_.price)) for _ in rate.rates],
        *[(_.name, lib.to_money(_.price)) for _ in rate.extraServices],
    ]

    return models.RateDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        service=service.name_or_key,
        total_charge=lib.to_money(rate.totalPrice),
        currency="USD",
        extra_charges=[
            models.ChargeDetails(name=name, currency="USD", amount=amount)
            for name, amount in charges
        ],
        meta=dict(
            service_name=service.name or mail_class,
            zone=lib.failsafe(lambda: rate.rates[0].zone),
        ),
    )


def rate_request(
    payload: models.RateRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    shipper = lib.to_address(payload.shipper)
    recipient = lib.to_address(payload.recipient)

    if shipper.country_code != units.Country.US.name:
        raise errors.OriginNotServicedError(shipper.country_code)

    if recipient.country_code == units.Country.US.name:
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

    # map data to convert karrio model to usps specific type
    request = [
        usps.RateRequestType(
            originZIPCode=shipper.postal_code,
            foreignPostalCode=recipient.postal_code,
            destinationCountryCode=recipient.country_code,
            weight=package.weight.LB,
            length=package.length.IN,
            width=package.width.IN,
            height=package.height.IN,
            mailClass=getattr(
                services.first, "value", provider_units.ShippingService.usps_all.value
            ),
            priceType=package.options.usps_price_type.state or "RETAIL",
            mailingDate=lib.fdate(
                package.options.shipment_date.state or time.strftime("%Y-%m-%d")
            ),
            accountType=settings.account_type or "EPS",
            accountNumber=lib.identity(
                settings.account_number or settings.connection_config.mailer_id.state
            ),
            itemValue=package.items.value_amount,
            extraServices=[
                lib.to_int(_.code)
                for __, _ in options.items()
                if __ not in provider_units.CUSTOM_OPTIONS
            ],
        )
        for package in packages
    ]

    return lib.Serializable(request, lib.to_dict)
