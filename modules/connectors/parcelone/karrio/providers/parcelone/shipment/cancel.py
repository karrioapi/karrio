"""Karrio ParcelOne shipment cancellation implementation."""

import typing
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.parcelone.error as error
import karrio.providers.parcelone.utils as provider_utils


def parse_shipment_cancel_response(
    _response: lib.Deserializable[dict],
    settings: provider_utils.Settings,
) -> typing.Tuple[typing.Optional[models.ConfirmationDetails], typing.List[models.Message]]:
    """Parse shipment cancellation response from ParcelOne REST API."""
    response = _response.deserialize()
    messages = error.parse_error_response(response, settings)
    success = response.get("success") == 1

    confirmation = lib.identity(
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
    """Create ParcelOne shipment cancel request.

    The API uses DELETE /shipment/{ShipmentRefField}/{ShipmentRefValue}
    where ShipmentRefField can be: ShipmentID, ShipmentRef, or TrackingID
    """
    # Determine which reference field to use based on identifier format
    identifier = payload.shipment_identifier

    # If it's a numeric string, it's likely a ShipmentID
    # If it starts with digits and has a specific length (13), it's likely a TrackingID
    # Otherwise, treat it as a ShipmentRef
    if identifier.isdigit() and len(identifier) < 10:
        ref_field = "ShipmentID"
    elif identifier.isdigit() and len(identifier) >= 10:
        ref_field = "TrackingID"
    else:
        ref_field = "ShipmentRef"

    request = dict(
        ref_field=ref_field,
        ref_value=identifier,
    )

    return lib.Serializable(request, lib.to_dict)
