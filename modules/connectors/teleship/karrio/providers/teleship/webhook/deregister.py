"""Karrio Teleship webhook deregistration implementation."""

import typing
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.teleship.error as error
import karrio.providers.teleship.utils as provider_utils


def parse_webhook_deregistration_response(
    _response: lib.Deserializable[str],
    settings: provider_utils.Settings,
) -> typing.Tuple[models.ConfirmationDetails, typing.List[models.Message]]:
    response = _response.deserialize()
    messages = error.parse_error_response(response, settings)

    # Teleship returns 204 No Content on successful deletion
    # or success response with status
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
            operation="webhook_deregistration",
        )
        if success
        else None
    )

    return confirmation, messages


def webhook_deregistration_request(
    payload: models.WebhookDeregistrationRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    """Create a Teleship webhook deregistration request"""

    request = {"webhookId": payload.webhook_id}

    return lib.Serializable(request, lib.to_dict)
