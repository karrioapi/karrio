"""Karrio Hermes pickup cancellation API implementation."""

import typing
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.hermes.error as error
import karrio.providers.hermes.utils as provider_utils


def parse_pickup_cancel_response(
    _response: lib.Deserializable[dict],
    settings: provider_utils.Settings,
) -> typing.Tuple[models.ConfirmationDetails, typing.List[models.Message]]:
    """Parse pickup cancellation response from carrier API"""
    response = _response.deserialize()
    messages = error.parse_error_response(response, settings)

    # Check if cancellation was successful
    success = _extract_cancellation_status(response)
    confirmation = (
        models.ConfirmationDetails(
            carrier_id=settings.carrier_id,
            carrier_name=settings.carrier_name,
            success=success,
            operation="Cancel Pickup",
        ) if success else None
    )

    return confirmation, messages


def _extract_cancellation_status(
    response: dict
) -> bool:
    """Extract cancellation success status from carrier response"""
    
    # Example implementation for JSON response:
    # return response.get("status", "").lower() == "cancelled"

    # For development, always return success
    return True
    


def pickup_cancel_request(
    payload: models.PickupCancelRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    """Create pickup cancellation request for carrier API"""
    # Extract cancellation details
    confirmation_number = payload.confirmation_number

    
    # Example implementation for JSON request:
    request = {
        "confirmationNumber": confirmation_number
    }

    return lib.Serializable(request, lib.to_dict)
    