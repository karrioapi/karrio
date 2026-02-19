"""Karrio SmartKargo shipment cancellation API implementation."""

import typing
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.smartkargo.error as error
import karrio.providers.smartkargo.utils as provider_utils


def parse_shipment_cancel_response(
    _response: lib.Deserializable[typing.List[typing.Tuple[str, dict]]],
    settings: provider_utils.Settings,
) -> typing.Tuple[models.ConfirmationDetails, typing.List[models.Message]]:
    """Parse shipment cancellation response from SmartKargo void API.

    For multi-piece shipments, receives a list of (tracking_number, response) tuples.
    Swagger response format per call: { result: { cancelled: boolean, messages: string } }
    """
    responses = _response.deserialize()

    messages: typing.List[models.Message] = sum(
        [
            error.parse_error_response(response, settings, tracking_number=tracking_number)
            for tracking_number, response in responses
        ],
        start=[],
    )

    # Check if any package was successfully cancelled (matches Sendle's pattern)
    success = any(_is_cancelled(response) for _, response in responses)

    # Collect result messages from failed cancellations
    for tracking_number, response in responses:
        result = response.get("result") or {}
        result_message = result.get("messages")
        if result_message and not _is_cancelled(response):
            messages.append(
                models.Message(
                    carrier_id=settings.carrier_id,
                    carrier_name=settings.carrier_name,
                    message=result_message,
                    details=dict(tracking_number=tracking_number),
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


def _is_cancelled(response: dict) -> bool:
    """Check if a single void response indicates successful cancellation."""
    result = response.get("result") or {}
    return (
        result.get("cancelled", False)
        or response.get("status", "").lower() == "success"
    )


def shipment_cancel_request(
    payload: models.ShipmentCancelRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    """Create a shipment cancellation request for SmartKargo void API.

    SmartKargo void endpoint requires prefix and airWaybill as query parameters.
    For multi-piece shipments, tracking numbers are collected from
    options.tracking_numbers (populated by lib.to_multi_piece_shipment in meta).

    The tracking number format is: {prefix}{airWaybill} (e.g., AXB01234567)
    """
    options = payload.options or {}

    # Use tracking_numbers from meta (populated by lib.to_multi_piece_shipment).
    # NOTE: payload.shipment_identifier is the packageReference, NOT a tracking number,
    # so we must NOT include it here.  For single-piece shipments (where
    # to_multi_piece_shipment doesn't add tracking_numbers to meta), fall back to
    # reconstructing from prefix + air_waybill stored in meta.
    tracking_numbers = list(set(options.get("tracking_numbers") or []))

    # Fallback for single-piece shipments: reconstruct from meta prefix + air_waybill
    if not tracking_numbers:
        prefix = options.get("prefix")
        air_waybill = options.get("air_waybill")
        if prefix and air_waybill:
            tracking_numbers = [f"{prefix}{air_waybill}"]

    # Optional parameters from Swagger spec
    user_name = options.get("user_name") or options.get("userName")
    reason = options.get("reason")

    # Build one cancel request per tracking number (filter Nones inline)
    request = [
        {
            k: v for k, v in dict(
                prefix=tracking_number[:3] if len(tracking_number) >= 11 else options.get("prefix"),
                airWaybill=tracking_number[3:] if len(tracking_number) >= 11 else options.get("air_waybill"),
                userName=user_name,
                reason=reason,
            ).items() if v is not None
        }
        for tracking_number in tracking_numbers
        if len(tracking_number) >= 11 or options.get("prefix")
    ]

    return lib.Serializable(request, lib.identity)
