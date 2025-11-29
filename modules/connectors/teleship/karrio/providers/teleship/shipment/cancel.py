"""Karrio Teleship shipment cancellation API implementation."""

import typing
import karrio.schemas.teleship.shipment_cancel_request as teleship_req
import karrio.schemas.teleship.shipment_cancel_response as teleship_res
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.teleship.error as error
import karrio.providers.teleship.utils as provider_utils


def parse_shipment_cancel_response(
    _response: lib.Deserializable[dict],
    settings: provider_utils.Settings,
) -> typing.Tuple[models.ConfirmationDetails, typing.List[models.Message]]:
    """Parse shipment cancellation response from carrier API"""
    response = _response.deserialize()
    messages = error.parse_error_response(response, settings)
    details = lib.to_object(teleship_res.ShipmentCancelResponseType, response)

    # Check if cancellation was successful based on status
    success = details.status in ["cancelled", "voided"] if details else False

    confirmation = lib.identity(
        models.ConfirmationDetails(
            carrier_id=settings.carrier_id,
            carrier_name=settings.carrier_name,
            operation="Cancel Shipment",
            success=success,
        )
        if details
        else None
    )

    return confirmation, messages


def shipment_cancel_request(
    payload: models.ShipmentCancelRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    """Create a shipment cancellation request for the carrier API"""

    request = teleship_req.ShipmentCancelRequestType(
        shipmentId=payload.shipment_identifier,
    )

    return lib.Serializable(request, lib.to_dict)
