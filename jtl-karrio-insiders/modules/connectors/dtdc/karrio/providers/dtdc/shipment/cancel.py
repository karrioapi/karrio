"""Karrio DTDC shipment cancellation implementation."""

import karrio.schemas.dtdc.shipment_cancel_request as dtdc_req
import karrio.schemas.dtdc.shipment_cancel_response as dtdc_res

import typing
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.dtdc.error as error
import karrio.providers.dtdc.utils as provider_utils
import karrio.providers.dtdc.units as provider_units


def parse_shipment_cancel_response(
    _response: lib.Deserializable[dict],
    settings: provider_utils.Settings,
) -> typing.Tuple[models.ConfirmationDetails, typing.List[models.Message]]:
    """Parse shipment cancellation response from DTDC API."""
    response = _response.deserialize()
    messages = error.parse_error_response(response, settings)

    success = response.get("success", False)

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
    """Create a shipment cancellation request for DTDC API."""

    # Build cancellation request
    request = dtdc_req.ShipmentCancelRequestType(
        AWBNo=[payload.shipment_identifier],
        customerCode=settings.customer_code,
    )

    return lib.Serializable(request, lib.to_dict)
