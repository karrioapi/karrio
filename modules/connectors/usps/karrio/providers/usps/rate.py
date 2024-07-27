"""Karrio USPS rating API implementation."""

import karrio.schemas.usps.rating_request as usps
import karrio.schemas.usps.rating_response as rating

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
                    _extract_details(rate["rateOptions"], settings)
                    for rate in responses
                    if rate.get("rateOptions") is not None
                ],
            )
            for _, response in enumerate(responses, start=1)
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

    shipper = lib.to_address(payload.shipper)
    recipient = lib.to_address(payload.recipient)
    packages = lib.to_packages(payload.parcels)
    services = lib.to_services(payload.services, provider_units.ShippingService)
    options = lib.to_shipping_options(
        payload.options,
        package_options=packages.options,
        initializer=provider_units.shipping_options_initializer,
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
                    services if any(services) else [provider_units.ShippingService.all]
                )
            ],
            priceType=options.usps.price_type.state,
            mailingDate=lib.fdate(
                options.shipment_date.state or time.strftime("%Y-%m-%d")
            ),
            accountType=settings.account_type or "EPS",
            accountNumber=settings.account_number,
            itemValue=package.items.value_amount,
            extraServices=[
                _.code
                for __, _ in options.items
                if _.name not in provider_units.CUSTOM_OPTIONS
            ],
        )
        for package in packages
    ]

    return lib.Serializable(request, lib.to_dict)
