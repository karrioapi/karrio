import karrio.schemas.australiapost.rate_request as australiapost
import karrio.schemas.australiapost.rate_response as rating
import typing
import karrio.lib as lib
import karrio.core.units as units
import karrio.core.models as models
import karrio.providers.australiapost.error as error
import karrio.providers.australiapost.utils as provider_utils
import karrio.providers.australiapost.units as provider_units


def parse_rate_response(
    _response: lib.Deserializable[dict],
    settings: provider_utils.Settings,
) -> typing.Tuple[typing.List[models.RateDetails], typing.List[models.Message]]:
    response = _response.deserialize()
    items = response.get("items") or []

    messages = sum(
        [
            error.parse_error_response(
                item,
                settings,
            )
            for item in items
            if "errors" in item or "warnings" in item
        ],
        start=error.parse_error_response(response, settings),
    )
    rates = [_extract_details(rate, settings) for rate in response if "prices" in rate]

    return rates, messages


def _extract_details(
    data: dict,
    settings: provider_utils.Settings,
) -> models.RateDetails:
    rate = lib.to_object(rating.PriceElementType, data)
    service = provider_units.ShippingService.map(rate.product_id)
    charges = [
        ("base charge", rate.calculated_price_ex_gst),
        ("GST", rate.calculated_gst),
        *[
            (_.type, _.attributes.price.calculated_price)
            for _ in rate.features.values()
            if lib.failsafe(lambda: _.attributes.price.calculated_price) is not None
        ],
    ]

    return models.RateDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        service=service.name_or_key,
        total_charge=lib.to_money(rate.calculated_price),
        currency=units.Currency.AUD.name,
        extra_charges=[
            models.ChargeDetails(
                name=name,
                amount=lib.to_money(value),
                currency=units.Currency.AUD.name,
            )
            for name, value in charges
        ],
        meta=dict(
            service_name=rate.product_type,
        ),
    )


def rate_request(
    payload: models.RateRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    options = lib.to_shipping_options(
        payload.options,
        option_type=provider_units.ShippingOption,
    )
    packages = lib.to_packages(
        payload.parcels,
        options=options,
    )
    services = lib.to_services(payload.services, provider_units.ShippingService)

    request = australiapost.RateRequestType(
        shipments=[
            australiapost.ShipmentType(
                shipment_from=australiapost.FromType(
                    suburb=payload.origin.suburb,
                    state=payload.origin.state,
                    postcode=payload.origin.postcode,
                ),
                to=australiapost.FromType(
                    suburb=payload.destination.suburb,
                    state=payload.destination.state,
                    postcode=payload.destination.postcode,
                ),
                items=[
                    australiapost.ItemType(
                        item_reference=None,
                        length=package.length.CM,
                        width=package.width.CM,
                        height=package.height.CM,
                        weight=package.weight.KG,
                        packaging_type=provider_units.PackagingType.map(
                            package.packaging_type
                        ).value,
                        product_ids=[_.value for _ in services],
                        features=(
                            {
                                [option.code]: australiapost.FeatureType(
                                    attributes=australiapost.AttributesType(
                                        cover_amount=option.value,
                                    ),
                                )
                                for option in package.options
                            }
                            if any(package.options)
                            else None
                        ),
                    )
                    for package in packages
                ],
            )
        ],
    )

    return lib.Serializable(
        request,
        lambda _: lib.to_dict(
            lib.to_json(_).replace("shipment_from", "from"),
        ),
    )
