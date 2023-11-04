import karrio.schemas.roadie.rate_request as roadie
import karrio.schemas.roadie.rate_response as rating
import typing
import datetime
import karrio.lib as lib
import karrio.core.units as units
import karrio.core.models as models
import karrio.providers.roadie.error as error
import karrio.providers.roadie.utils as provider_utils
import karrio.providers.roadie.units as provider_units


def parse_rate_response(
    _response: lib.Deserializable[dict],
    settings: provider_utils.Settings,
) -> typing.Tuple[typing.List[models.RateDetails], typing.List[models.Message]]:
    response = _response.deserialize()
    messages = error.parse_error_response(response, settings)
    rates = (
        [_extract_details(response, settings)] if response.get("errors") is None else []
    )

    return rates, messages


def _extract_details(
    data: dict,
    settings: provider_utils.Settings,
) -> models.RateDetails:
    rate = lib.to_object(rating.RateResponse, data)

    return models.RateDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        service=provider_units.ShippingService.roadie_local_delivery.name,
        total_charge=lib.to_money(rate.price),
        currency=units.Currency.USD.name,
        transit_days=1,
        extra_charges=[
            models.ChargeDetails(
                name="Base Price",
                currency=units.Currency.USD.name,
                amount=lib.to_money(rate.price),
            )
        ],
        meta=dict(
            service_name=provider_units.ShippingService.roadie_local_delivery.value,
            estimated_distance=rate.estimated_distance,
            size=rate.size,
        ),
    )


def rate_request(
    payload: models.RateRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    shipper = lib.to_address(payload.shipper)
    recipient = lib.to_address(payload.recipient)
    packages = lib.to_packages(payload.parcels)
    options = lib.to_shipping_options(
        payload.options,
        package_options=packages.options,
        initializer=provider_units.shipping_options_initializer,
    )

    pickup_after = lib.to_date(
        options.pickup_after.state or datetime.datetime.now(),
        current_format="%Y-%m-%d %H:%M:%S",
    )
    deliver_start = lib.fdatetime(
        options.deliver_start.state or (pickup_after + datetime.timedelta(minutes=30)),
        current_format="%Y-%m-%d %H:%M:%S",
        output_format="%Y-%m-%dT%H:%M:%SZ",
    )
    deliver_end = lib.fdatetime(
        options.deliver_end.state or (pickup_after + datetime.timedelta(minutes=60)),
        current_format="%Y-%m-%d %H:%M:%S",
        output_format="%Y-%m-%dT%H:%M:%SZ",
    )

    request = roadie.RateRequest(
        items=[
            roadie.Item(
                length=package.length.IN,
                width=package.width.IN,
                height=package.height.IN,
                weight=package.weight.LB,
                quantity=(
                    package.items.quantity if package.items.quantity or 0 > 0 else 1
                ),
                value=options.declared_value.state or 0.0,
            )
            for package in packages
        ],
        pickup_location=roadie.Location(
            address=roadie.Address(
                street1=shipper.address_line,
                city=shipper.city,
                state=shipper.state_code,
                zip=shipper.postal_code,
            ),
        ),
        delivery_location=roadie.Location(
            address=roadie.Address(
                street1=recipient.address_line,
                city=recipient.city,
                state=recipient.state_code,
                zip=recipient.postal_code,
            ),
        ),
        pickup_after=lib.fdatetime(pickup_after, output_format="%Y-%m-%dT%H:%M:%SZ"),
        deliver_between=roadie.DeliverBetween(
            start=deliver_start,
            end=deliver_end,
        ),
    )

    return lib.Serializable(request, lib.to_dict)
