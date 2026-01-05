"""Karrio Asendia shipment cancellation API implementation."""

import typing
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.asendia.error as error
import karrio.providers.asendia.utils as provider_utils


def parse_shipment_cancel_response(
    _response: lib.Deserializable[dict],
    settings: provider_utils.Settings,
) -> typing.Tuple[typing.Optional[models.ConfirmationDetails], typing.List[models.Message]]:
    """Parse shipment cancellation response from Asendia API."""
    response = _response.deserialize()
    messages = error.parse_error_response(response, settings)

    # Asendia DELETE returns empty response on success (HTTP 204)
    # If no error messages, consider it successful
    success = len(messages) == 0

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
    """Create a shipment cancellation request for Asendia API.

    Asendia uses DELETE /api/parcels/{parcelId} endpoint.
    The shipment_identifier should be the parcel ID returned from create.
    """
    # Return the parcel ID to be used in the DELETE URL
    return lib.Serializable(payload.shipment_identifier)
