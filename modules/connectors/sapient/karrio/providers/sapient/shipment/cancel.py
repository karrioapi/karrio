import typing
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.sapient.error as error
import karrio.providers.sapient.utils as provider_utils
import karrio.providers.sapient.units as provider_units


def parse_shipment_cancel_response(
    _response: lib.Deserializable[dict],
    settings: provider_utils.Settings,
) -> typing.Tuple[models.ConfirmationDetails, typing.List[models.Message]]:
    response = _response.deserialize()
    messages = error.parse_error_response(response, settings)
    success = response.get("ok") is True

    confirmation = (
        models.ConfirmationDetails(
            carrier_id=settings.carrier_id,
            carrier_name=settings.carrier_name,
            operation="Cancel Shipment",
            success=success,
        )
        if success
        else None
    )

    return confirmation, messages


def shipment_cancel_request(
    payload: models.ShipmentCancelRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    options = lib.units.Options(
        payload.options,
        option_type=lib.units.create_enum(
            "PickupOptions",
            # fmt: off
            {
                "reason": lib.OptionEnum("Reason"),
                "shipment_ids": lib.OptionEnum("ShipmentIds", list),
            },
            # fmt: on
        ),
    )

    # map data to convert karrio model to sapient specific type
    request = dict(
        Status="Cancel",
        Reason=options.reason.state or "Order Cancelled",
        ShipmentIds=lib.identity(
            options.shipment_ids.state or [payload.shipment_identifier]
        ),
    )

    return lib.Serializable(request, lib.to_dict)
