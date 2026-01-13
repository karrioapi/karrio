"""Karrio Spring shipment cancellation API implementation."""

import karrio.schemas.spring.shipment_cancel_request as spring_req

import typing
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.spring.error as error
import karrio.providers.spring.utils as provider_utils


def parse_shipment_cancel_response(
    _response: lib.Deserializable[dict],
    settings: provider_utils.Settings,
) -> typing.Tuple[models.ConfirmationDetails, typing.List[models.Message]]:
    """Parse VoidShipment response from Spring API."""
    response = _response.deserialize()
    messages = error.parse_error_response(response, settings)

    # ErrorLevel 0 means success
    success = response.get("ErrorLevel") == 0 and not any(messages)

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
    """Create a VoidShipment request for Spring API."""

    # Spring API allows either TrackingNumber or ShipperReference
    # payload.shipment_identifier is used as TrackingNumber
    request = spring_req.ShipmentCancelRequestType(
        Apikey=settings.api_key,
        Command="VoidShipment",
        Shipment=spring_req.ShipmentType(
            TrackingNumber=payload.shipment_identifier,
        ),
    )

    return lib.Serializable(request, lib.to_dict)
    
