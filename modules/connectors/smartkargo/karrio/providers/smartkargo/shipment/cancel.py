"""Karrio SmartKargo shipment cancellation API implementation."""

import typing
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.smartkargo.error as error
import karrio.providers.smartkargo.utils as provider_utils


def parse_shipment_cancel_response(
    _response: lib.Deserializable[dict],
    settings: provider_utils.Settings,
) -> typing.Tuple[models.ConfirmationDetails, typing.List[models.Message]]:
    """Parse shipment cancellation response from SmartKargo void API.

    Swagger response format: { result: { cancelled: boolean, messages: string } }
    """
    response = _response.deserialize()
    messages = error.parse_error_response(response, settings)

    # SmartKargo void returns { result: { cancelled: bool, messages: str } }
    result = response.get("result") or {}
    is_cancelled = result.get("cancelled", False)

    # Also check for legacy format { status: "success" } for backwards compatibility
    is_legacy_success = response.get("status", "").lower() == "success"

    success = (is_cancelled or is_legacy_success) and not any(messages)

    # Add any messages from the result to our messages list
    result_message = result.get("messages")
    if result_message and not success:
        messages.append(
            models.Message(
                carrier_id=settings.carrier_id,
                carrier_name=settings.carrier_name,
                message=result_message,
            )
        )

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
    """Create a shipment cancellation request for SmartKargo void API.

    SmartKargo void endpoint requires prefix and airWaybill as query parameters.
    Optional parameters: userName (for audit log), reason (cancellation reason).

    These can be provided via:
    1. options.prefix and options.air_waybill
    2. Parsed from shipment_identifier if it's the tracking number format ({prefix}{airWaybill})

    The tracking number format is typically: AXB01234567 (3-char prefix + 8-digit airWaybill)
    """
    options = payload.options or {}

    # Try to get prefix and air_waybill from options first
    prefix = options.get("prefix")
    air_waybill = options.get("air_waybill")

    # If not provided, try to parse from shipment_identifier
    # SmartKargo tracking numbers are typically: {prefix}{airWaybill} (e.g., AXB01234567)
    if not prefix or not air_waybill:
        identifier = payload.shipment_identifier or ""
        if len(identifier) >= 11:  # 3-char prefix + 8-digit airWaybill
            prefix = prefix or identifier[:3]
            air_waybill = air_waybill or identifier[3:]

    # Optional parameters from Swagger spec
    user_name = options.get("user_name") or options.get("userName")
    reason = options.get("reason")

    request = dict(
        prefix=prefix,
        airWaybill=air_waybill,
        userName=user_name,
        reason=reason,
    )

    return lib.Serializable(request, lib.to_dict)
