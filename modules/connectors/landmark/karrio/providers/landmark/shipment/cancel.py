"""Karrio Landmark Global shipment cancellation implementation."""

import karrio.schemas.landmark.cancel_request as cancel_req
import karrio.schemas.landmark.cancel_response as cancel_res

import typing
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.landmark.error as error
import karrio.providers.landmark.utils as provider_utils


def parse_shipment_cancel_response(
    _response: lib.Deserializable[lib.Element],
    settings: provider_utils.Settings,
) -> typing.Tuple[models.ConfirmationDetails, typing.List[models.Message]]:
    response = _response.deserialize()
    messages = error.parse_error_response(response, settings)

    cancellation = (
        _extract_cancellation_details(response, settings)
        if len(messages) == 0
        else None
    )

    return cancellation, messages


def _extract_cancellation_details(
    data: lib.Element,
    settings: provider_utils.Settings,
) -> models.ConfirmationDetails:
    """Extract cancellation confirmation details from CancelResponse"""
    cancel_response = lib.to_object(cancel_res.CancelResponse, data)
    result = cancel_response.Result

    if not result or not result.Success:
        return None

    return models.ConfirmationDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        operation="Shipment Cancellation",
        success=result.Success,
    )


def shipment_cancel_request(
    payload: models.ShipmentCancelRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    """Create a shipment cancellation request for the carrier API"""

    request = cancel_req.CancelRequest(
        Login=cancel_req.LoginType(
            Username=settings.username,
            Password=settings.password,
        ),
        Test=settings.test_mode,
        ClientID=settings.client_id,
        TrackingNumber=payload.shipment_identifier,
        DeleteShipment=True,
        Reason=lib.identity(
            payload.options.get("reason")
            or "Consignee canceled shipment."
        ),
    )

    return lib.Serializable(request, lib.to_xml)
