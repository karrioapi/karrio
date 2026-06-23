"""Karrio ParcelOne shipment cancellation implementation."""

import karrio.core.models as models
import karrio.lib as lib
import karrio.providers.parcelone.error as error
import karrio.providers.parcelone.utils as provider_utils
import karrio.schemas.parcelone.cancel_response as cancel


def parse_shipment_cancel_response(
    _response: lib.Deserializable[dict],
    settings: provider_utils.Settings,
) -> tuple[models.ConfirmationDetails | None, list[models.Message]]:
    """Parse shipment cancellation response from ParcelOne REST API."""
    response = _response.deserialize()
    messages = error.parse_error_response(response, settings)

    cancel_response = lib.to_object(cancel.CancelResponseType, response)
    result = cancel_response.results
    success = cancel_response.success == 1 and (result.Success == 1 if result else False)

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

    DELETE /shipment/{ShipmentRefField}/{ShipmentRefValue}
    where ShipmentRefField is one of (lowercase per API spec):
    shipmentid, shipmentref, trackingid.
    """
    identifier = payload.shipment_identifier
    # 13-digit numeric → tracking number; shorter numeric → shipmentid; else ref.
    ref_field = lib.identity(
        "trackingid"
        if identifier.isdigit() and len(identifier) >= 10
        else "shipmentid"
        if identifier.isdigit()
        else "shipmentref"
    )

    return lib.Serializable(
        dict(ref_field=ref_field, ref_value=identifier),
        lib.to_dict,
    )
