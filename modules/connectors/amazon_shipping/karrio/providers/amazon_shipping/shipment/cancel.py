"""Karrio Amazon Shipping shipment cancellation implementation."""

import karrio.core.models as models
import karrio.lib as lib
import karrio.providers.amazon_shipping.error as error
import karrio.providers.amazon_shipping.utils as provider_utils


def parse_shipment_cancel_response(
    _response: lib.Deserializable[dict],
    settings: provider_utils.Settings,
) -> tuple[models.ConfirmationDetails, list[models.Message]]:
    """Parse shipment cancellation response (success = no errors). See SPECS.md."""
    response = _response.deserialize()
    messages = error.parse_error_response(response, settings)

    success = len(messages) == 0

    details = (
        models.ConfirmationDetails(
            carrier_id=settings.carrier_id,
            carrier_name=settings.carrier_name,
            success=success,
            operation="Cancel Shipment",
        )
        if success
        else None
    )

    return details, messages


def shipment_cancel_request(
    payload: models.ShipmentCancelRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    """Serialize the shipment id for the cancel API path. See SPECS.md."""
    return lib.Serializable(payload.shipment_identifier)
