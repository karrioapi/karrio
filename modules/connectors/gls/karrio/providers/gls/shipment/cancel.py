"""Karrio GLS Group shipment cancel implementation."""

import karrio.core.models as models
import karrio.lib as lib
import karrio.providers.gls.error as error
import karrio.providers.gls.utils as provider_utils


def parse_shipment_cancel_response(
    _response: lib.Deserializable[dict],
    settings: provider_utils.Settings,
) -> tuple[models.ConfirmationDetails | None, list[models.Message]]:
    """Parse the response of a CancelParcelByID call."""
    response = _response.deserialize()
    messages = error.parse_error_response(response, settings)
    success = not any(messages) and bool(response.get("TrackID"))

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
) -> lib.Serializable[str]:
    """Build the cancel request — the proxy interpolates the TrackID into
    the URL, so the serializable just carries the identifier string."""
    return lib.Serializable(payload.shipment_identifier)
