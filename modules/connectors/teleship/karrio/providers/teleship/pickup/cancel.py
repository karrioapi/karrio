"""Karrio Teleship pickup cancellation implementation."""

import typing
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.teleship.error as error
import karrio.providers.teleship.utils as provider_utils


def parse_cancel_pickup_response(
    _response: lib.Deserializable[str],
    settings: provider_utils.Settings,
) -> typing.Tuple[models.ConfirmationDetails, typing.List[models.Message]]:
    response = _response.deserialize()
    messages = error.parse_error_response(response, settings)

    success = not any(messages) and (
        isinstance(response, dict) and response.get("success") is not False
        or response == ""
        or response is None
    )

    confirmation = (
        models.ConfirmationDetails(
            carrier_id=settings.carrier_id,
            carrier_name=settings.carrier_name,
            success=success,
            operation="pickup_cancellation",
        )
        if success
        else None
    )

    return confirmation, messages


def cancel_pickup_request(
    payload: models.PickupCancelRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    request = {"pickupId": payload.confirmation_number}

    return lib.Serializable(request, lib.to_dict)
