import karrio.schemas.sendle.product_request as sendle
import karrio.schemas.sendle.product_response as rating
import typing
import karrio.lib as lib
import karrio.core.units as units
import karrio.core.models as models
import karrio.providers.sendle.error as error
import karrio.providers.sendle.utils as provider_utils
import karrio.providers.sendle.units as provider_units


def parse_rate_response(
    _response: lib.Deserializable[typing.List[dict]],
    settings: provider_utils.Settings,
) -> typing.Tuple[typing.List[models.RateDetails], typing.List[models.Message]]:
    responses = _response.deserialize()

    package_rates: typing.List[typing.Tuple[str, typing.List[models.RateDetails]]] = [
        (
            f"{_}",
            [
                _extract_details(rate, settings)
                for rate in (response if isinstance(response, list) else [response])
                if rate.get("quote") is not None
            ],
        )
        for _, response in enumerate(responses, start=1)
    ]

    messages = error.parse_error_response(responses, settings)
    rates = lib.to_multi_piece_rates(package_rates)

    return rates, messages


def _extract_details(
    data: dict,
    settings: provider_utils.Settings,
) -> models.RateDetails:
    rate = lib.to_object(rating.ProductResponseElementType, data)
    service = provider_units.ShippingService.map(rate.product.code)
    currency = rate.quote.gross.currency
    charges = [
        *[
            (name, lib.to_money(value["amount"]))
            for name, value in lib.to_dict(rate.price_breakdown).items()
            if lib.to_money(value["amount"]) > 0
        ],
        *[
            (name, lib.to_money(value["amount"]))
            for name, value in lib.to_dict(rate.tax_breakdown).items()
            if lib.to_money(value["amount"]) > 0
        ],
    ]

    return models.RateDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        service=service.name_or_key,
        total_charge=lib.to_money(rate.quote.gross.amount),
        currency=currency,
        transit_days=rate.eta.days_range[-1],
        extra_charges=[
            models.ChargeDetails(
                name=name,
                amount=value,
                currency=currency,
            )
            for name, value in charges
        ],
        meta=dict(
            service_name=service.name or rate.product.name,
            days_range=rate.eta.days_range,
            date_range=rate.eta.date_range,
            plan=rate.plan,
        ),
    )


def rate_request(
    payload: models.RateRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    shipper = lib.to_address(payload.shipper)
    recipient = lib.to_address(payload.recipient)
    options = lib.to_shipping_options(
        payload.options,
        option_type=provider_units.ShippingOption,
    )
    packages = lib.to_packages(
        payload.parcels,
        options=options,
        package_option_type=provider_units.ShippingOption,
        shipping_options_initializer=provider_units.shipping_options_initializer,
    )

    request = [
        sendle.ProductRequestType(
            sender_address_line1=shipper.address_line1,
            sender_address_line2=shipper.address_line2,
            sender_suburb=shipper.city,
            sender_postcode=shipper.postal_code,
            sender_country=shipper.country_code,
            receiver_address_line1=recipient.address_line1,
            receiver_address_line2=recipient.address_line2,
            receiver_suburb=recipient.city,
            receiver_postcode=recipient.postal_code,
            receiver_country=recipient.country_code,
            weight_value=package.weight.KG,
            weight_units=units.WeightUnit.KG.name.lower(),
            volume_value=package.volume.m3,
            volume_units=units.VolumeUnit.m3.name,
            length_value=package.length.CM,
            width_value=package.width.CM,
            height_value=package.height.CM,
            dimension_units=units.DimensionUnit.CM.name.lower(),
        )
        for package in packages
    ]

    return lib.Serializable(request, lib.to_dict)
