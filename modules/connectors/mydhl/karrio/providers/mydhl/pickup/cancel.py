"""Karrio MyDHL pickup cancellation API implementation."""

import typing
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.mydhl.error as error
import karrio.providers.mydhl.utils as provider_utils
import karrio.schemas.mydhl.pickup_cancel_response as cancel_res


def parse_pickup_cancel_response(
    _response: lib.Deserializable[dict],
    settings: provider_utils.Settings,
) -> typing.Tuple[models.ConfirmationDetails, typing.List[models.Message]]:
    """Parse pickup cancellation response from MyDHL API"""
    response = _response.deserialize()
    messages = error.parse_error_response(response, settings)

    cancel_response = lib.to_object(cancel_res.PickupCancelResponseType, response)
    confirmation = _extract_details(cancel_response, settings)

    return confirmation, messages


def _extract_details(
    cancel: cancel_res.PickupCancelResponseType,
    settings: provider_utils.Settings,
) -> models.ConfirmationDetails:
    """Extract cancellation confirmation from MyDHL cancel response"""
    # MyDHL returns status for successful cancellation
    success = bool(cancel.status and cancel.dispatchConfirmationNumber)

    return models.ConfirmationDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        success=success,
        operation="Cancel Pickup",
    )
    


def pickup_cancel_request(
    payload: models.PickupCancelRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    """Create pickup cancellation request for MyDHL API"""
    # MyDHL uses DELETE /pickups/{confirmationNumber}
    # So we just return the confirmation number
    return lib.Serializable(payload.confirmation_number)
    