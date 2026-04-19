import karrio.core.models as models
import karrio.core.units as units
import karrio.lib as lib
import karrio.providers.australiapost.error as error
import karrio.providers.australiapost.units as provider_units
import karrio.providers.australiapost.utils as provider_utils
import karrio.schemas.australiapost.rate_request as australiapost
import karrio.schemas.australiapost.rate_response as rating


def parse_rate_response(
    _response: lib.Deserializable[dict],
    settings: provider_utils.Settings,
) -> tuple[list[models.RateDetails], list[models.Message]]:
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
    rates = lib.to_multi_piece_rates(
        [
            (
                f"{_}",
                [_extract_details(price, settings) for price in item.get("prices") or []],
            )
            for _, item in enumerate(items, start=1)
        ]
    )

    return rates, messages


def _extract_details(
    data: dict,
    settings: provider_utils.Settings,
) -> models.RateDetails:
    rate = lib.to_object(rating.PriceElementType, data)
    service = provider_units.ShippingService.map(rate.product_id)
    features = data.get("features") or {}
    feature_charges = []
    for feature in features.values():
        feature_price = lib.failsafe(lambda feature=feature: feature.attributes.price.calculated_price)
        if feature_price is not None:
            feature_charges.append((feature.type, feature_price))

    charges = [
        ("base charge", rate.calculated_price_ex_gst),
        ("GST", rate.calculated_gst),
        *feature_charges,
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
            if value
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
        initializer=provider_units.shipping_options_initializer,
    )
    packages = lib.to_packages(
        payload.parcels,
        options=options,
        package_option_type=provider_units.ShippingOption,
        shipping_options_initializer=provider_units.shipping_options_initializer,
    )
    services = lib.to_services(payload.services, provider_units.ShippingService)

    request = australiapost.RateRequestType(
        rate_request_from=australiapost.FromType(
            postcode=payload.shipper.postal_code,
            country=payload.shipper.country_code,
        ),
        to=australiapost.FromType(
            postcode=payload.recipient.postal_code,
            country=payload.recipient.country_code,
        ),
        items=[
            australiapost.ItemType(
                item_reference=(getattr(package.parcel, "id", None) or str(idx)),
                length=package.length.CM,
                width=package.width.CM,
                height=package.height.CM,
                weight=package.weight.KG,
                packaging_type=provider_units.PackagingType.map(package.packaging_type).value,
                product_ids=[_.value for _ in services],
                features=lib.identity(
                    dict(
                        TRANSIT_COVER=dict(
                            attributes=dict(
                                cover_amount=package.options.australiapost_transit_cover.state,
                            ),
                        )
                    )
                    if (package.options.australiapost_transit_cover.state is not None)
                    else None
                ),
            )
            for idx, package in enumerate(packages, start=1)
        ],
    )

    return lib.Serializable(
        request,
        lambda _: lib.to_dict(
            lib.to_json(_).replace("rate_request_from", "from"),
        ),
    )
