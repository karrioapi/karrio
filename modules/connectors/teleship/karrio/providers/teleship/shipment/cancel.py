"""Karrio Teleship shipment cancellation API implementation."""
import typing
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.teleship.error as error
import karrio.providers.teleship.utils as provider_utils
import karrio.providers.teleship.units as provider_units


def parse_shipment_cancel_response(
    _response: lib.Deserializable[dict],
    settings: provider_utils.Settings,
) -> typing.Tuple[models.ConfirmationDetails, typing.List[models.Message]]:
    """
    Parse shipment cancellation response from carrier API

    _response: The carrier response to deserialize
    settings: The carrier connection settings

    Returns a tuple with (ConfirmationDetails, List[Message])
    """
    response = _response.deserialize()
    messages = error.parse_error_response(response, settings)

    # Extract success state from the response
    success = _extract_cancellation_status(response)

    # Create confirmation details if successful
    confirmation = (
        models.ConfirmationDetails(
            carrier_id=settings.carrier_id,
            carrier_name=settings.carrier_name,
            operation="Cancel Shipment",
            success=success,
        ) if success else None
    )

    return confirmation, messages


def _extract_cancellation_status(
    response: dict
) -> bool:
    """
    Extract cancellation success status from the carrier response

    response: The deserialized carrier response

    Returns True if cancellation was successful, False otherwise
    """
    
    # Example implementation for JSON response:
    # return response.get("success", False)

    # For development, always return success
    return True
    


def shipment_cancel_request(
    payload: models.ShipmentCancelRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    """
    Create a shipment cancellation request for the carrier API

    payload: The standardized ShipmentCancelRequest from karrio
    settings: The carrier connection settings

    Returns a Serializable object that can be sent to the carrier API
    """
    
    # Create JSON request for shipment cancellation
    # Example implementation:
    # import karrio.schemas.teleship.shipment_cancel_request as teleship_req
    #
    # request = teleship_req.ShipmentCancelRequestType(
    #     shipmentId=payload.shipment_identifier,
    #     accountNumber=settings.account_number,
    #     # Add any other required fields
    # )
    #
    # return lib.Serializable(request, lib.to_dict)

    # For development, return a simple JSON request
    request = {
        "shipmentId": payload.shipment_identifier
    }

    return lib.Serializable(request, lib.to_dict)
    
