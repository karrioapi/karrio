"""Karrio Easyship pickup API implementation."""

import karrio.schemas.easyship.pickup_request as easyship
import karrio.schemas.easyship.pickup_response as pickup

import typing
import karrio.lib as lib
import karrio.core.units as units
import karrio.core.models as models
import karrio.providers.easyship.error as error
import karrio.providers.easyship.utils as provider_utils
import karrio.providers.easyship.units as provider_units


def parse_pickup_response(
    _response: lib.Deserializable[dict],
    settings: provider_utils.Settings,
) -> typing.Tuple[typing.List[models.PickupDetails], typing.List[models.Message]]:
    response = _response.deserialize()

    messages = error.parse_error_response(response, settings)
    pickup = lib.identity(
        _extract_details(response, settings)
        if response.get("pickup") is not None
        else None
    )

    return pickup, messages


def _extract_details(
    data: dict,
    settings: provider_utils.Settings,
) -> models.PickupDetails:
    details = lib.to_object(pickup.PickupResponseType, data)

    return models.PickupDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        confirmation_number=details.pickup.easyship_pickup_id,
        pickup_date=lib.fdate(details.pickup.selected_from_time, "%Y-%m-%dT%H:%M"),
        ready_time=lib.ftime(details.pickup.selected_from_time, "%Y-%m-%dT%H:%M"),
        closing_time=lib.ftime(details.pickup.selected_to_time, "%Y-%m-%dT%H:%M"),
        meta=dict(
            easyship_courier_id=details.pickup.courier.id,
            easyship_pickup_id=details.pickup.easyship_pickup_id,
            easyship_shipment_ids=details.meta.easyship_shipment_ids,
        ),
    )


def pickup_request(
    payload: models.PickupRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    options = lib.units.Options(
        payload.options,
        option_type=lib.units.create_enum(
            "PickupOptions",
            {
                "shipments": lib.OptionEnum("shipments", list),
                "easyship_time_slot_id": lib.OptionEnum("time_slot_id", str),
                "shipment_identifiers": lib.OptionEnum("shipment_identifiers", list),
                "easyship_courier_account_id": lib.OptionEnum(
                    "courier_account_id", str
                ),
            },
        ),
    )
    easyship_shipment_ids = lib.identity(
        [_["shipment_identifier"] for _ in options.shipments.state]
        if any(options.shipments.state or [])
        else options.shipment_identifiers.state
    )

    # map data to convert karrio model to easyship specific type
    request = easyship.PickupRequestType(
        easyship_shipment_ids=easyship_shipment_ids,
        time_slot_id=options.easyship_time_slot_id.state,
        courier_id=options.easyship_courier_account_id.state,
        selected_from_time=lib.ftime(payload.ready_time, "%H:%M"),
        selected_to_time=lib.ftime(payload.closing_time, "%H:%M"),
        selected_date=lib.fdate(payload.pickup_date),
    )

    return lib.Serializable(request, lib.to_dict)
