import karrio.core.models as models
import karrio.lib as lib
import karrio.providers.canadapost.error as provider_error
import karrio.providers.canadapost.utils as provider_utils


def parse_shipment_cancel_response(
    _responses: lib.Deserializable[list[tuple[str, lib.Element]]],
    settings: provider_utils.Settings,
) -> tuple[models.ConfirmationDetails, list[models.Message]]:
    responses = [
        (_, provider_error.parse_error_response(response, settings, shipment_id=_))
        for _, response in _responses.deserialize()
    ]
    messages: list[models.Message] = sum([__ for _, __ in responses], start=[])
    success = any([len(errors) == 0 for _, errors in responses])

    confirmation: models.ConfirmationDetails = (
        models.ConfirmationDetails(
            carrier_id=settings.carrier_id,
            carrier_name=settings.carrier_name,
            success=success,
            operation="Cancel Shipment",
        )
        if success
        else None
    )

    return confirmation, messages


def shipment_cancel_request(payload: models.ShipmentCancelRequest, _) -> lib.Serializable:
    options = payload.options or {}
    request = list(
        set(
            [
                payload.shipment_identifier,
                *(options.get("shipment_identifiers") or []),
            ]
        )
    )

    return lib.Serializable(
        request,
        lib.identity,
        dict(email=options.get("email")),
    )
