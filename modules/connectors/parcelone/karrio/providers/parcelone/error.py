"""Karrio ParcelOne error parser."""

import typing
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.parcelone.utils as provider_utils


def parse_error_response(
    response: dict,
    settings: provider_utils.Settings,
    **details,
) -> typing.List[models.Message]:
    """Parse error response from ParcelOne REST API."""
    results = response.get("results") or {}
    action_result = results.get("ActionResult") or results

    # Collect all errors using list comprehensions
    errors: typing.List[dict] = sum(
        [
            # Top-level API errors
            [
                *[
                    {
                        "code": e.get("ErrorNo") or e.get("StatusCode"),
                        "message": e.get("Message"),
                        "instance": response.get("instance"),
                        "uniq_id": response.get("UniqId"),
                    }
                    for e in (response.get("errors") or [])
                ],
                # Top-level error message when no specific errors
                *(
                    [
                        {
                            "code": str(response.get("status", "")),
                            "message": response.get("message"),
                            "instance": response.get("instance"),
                            "uniq_id": response.get("UniqId"),
                        }
                    ]
                    if (
                        response.get("success") == -1
                        or response.get("type") == "error"
                    )
                    and not response.get("errors")
                    and response.get("message")
                    else []
                ),
            ],
            # ActionResult errors
            [
                {
                    "code": e.get("ErrorNo") or e.get("StatusCode"),
                    "message": e.get("Message"),
                    "shipment_id": action_result.get("ShipmentID"),
                    "tracking_id": action_result.get("TrackingID"),
                }
                for e in (action_result.get("Errors") or [])
                if isinstance(action_result, dict)
            ],
        ],
        [],
    )

    return [
        models.Message(
            carrier_id=settings.carrier_id,
            carrier_name=settings.carrier_name,
            code=error.get("code"),
            message=error.get("message"),
            details=lib.to_dict({**details, **{k: v for k, v in error.items() if k not in ("code", "message")}}),
        )
        for error in errors
        if error.get("code") or error.get("message")
    ]
