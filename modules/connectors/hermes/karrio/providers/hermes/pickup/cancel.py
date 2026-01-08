"""Karrio Hermes pickup cancellation API implementation."""

import typing
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.hermes.error as error
import karrio.providers.hermes.utils as provider_utils


def parse_pickup_cancel_response(
    _response: lib.Deserializable[dict],
    settings: provider_utils.Settings,
) -> typing.Tuple[typing.Optional[models.ConfirmationDetails], typing.List[models.Message]]:
    """Parse Hermes pickup cancellation response."""
    response = _response.deserialize()
    messages = error.parse_error_response(response, settings)

    # Check if cancellation was successful (no errors means success)
    success = len(messages) == 0

    confirmation = None
    if success:
        confirmation = models.ConfirmationDetails(
            carrier_id=settings.carrier_id,
            carrier_name=settings.carrier_name,
            success=True,
            operation="Cancel Pickup",
        )

    return confirmation, messages


def pickup_cancel_request(
    payload: models.PickupCancelRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    """Create Hermes pickup cancellation request.

    Note: The pickup order ID is passed in the URL path, not in the body.
    The proxy.cancel_pickup method extracts pickupOrderID from the payload.
    """
    # Hermes uses DELETE /pickuporders/{pickupOrderID}
    # The confirmation_number from Karrio is the pickupOrderID
    request = {
        "pickupOrderID": payload.confirmation_number,
    }

    return lib.Serializable(request, lib.to_dict)
    