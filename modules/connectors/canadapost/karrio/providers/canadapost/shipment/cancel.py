import karrio.schemas.canadapost.shipment as canadapost
import typing
import karrio.lib as lib
import karrio.core.units as units
import karrio.core.errors as errors
import karrio.core.models as models
import karrio.providers.canadapost.error as provider_error
import karrio.providers.canadapost.units as provider_units
import karrio.providers.canadapost.utils as provider_utils


def parse_shipment_cancel_response(
    _responses: lib.Deserializable[typing.List[typing.Tuple[str, lib.Element]]],
    settings: provider_utils.Settings,
) -> typing.Tuple[models.ConfirmationDetails, typing.List[models.Message]]:
    responses = [
        (_, provider_error.parse_error_response(response, settings, shipment_id=_))
        for _, response in _responses.deserialize()
    ]
    messages: typing.List[models.Message] = sum([__ for _, __ in responses], start=[])
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


def shipment_cancel_request(
    payload: models.ShipmentCancelRequest, _
) -> lib.Serializable:
    request = list(
        set(
            [
                payload.shipment_identifier,
                *((payload.options or {}).get("shipment_identifiers") or []),
            ]
        )
    )

    return lib.Serializable(
        request,
        lib.identity,
        dict(email=payload.options.get("email")),
    )
