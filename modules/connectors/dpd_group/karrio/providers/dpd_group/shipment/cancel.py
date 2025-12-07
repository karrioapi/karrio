"""Karrio DPD Group shipment cancellation implementation."""

import typing
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.dpd_group.error as error
import karrio.providers.dpd_group.utils as provider_utils


def parse_shipment_cancel_response(
    _response: lib.Deserializable,
    settings: provider_utils.Settings,
) -> typing.Tuple[models.ConfirmationDetails, typing.List[models.Message]]:
    response = _response.deserialize()
    messages = error.parse_error_response(response, settings)
    
    if messages:
        return None, messages
    
    return models.ConfirmationDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        operation="Cancel Shipment",
        success=True,
    ), []


def shipment_cancel_request(
    payload: models.ShipmentCancelRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    return lib.Serializable(payload.shipment_identifier)
