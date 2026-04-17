"""Karrio SmartKargo error parser."""

import typing
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.smartkargo.utils as provider_utils

_ERROR_STATUSES = {"ERROR", "FAILED", "REJECTED"}
_SUCCESS_STATUSES = {"PROCESSED", "QUOTED", "SUCCESS", "OK", ""}


def parse_error_response(
    response: typing.Union[dict, typing.List[dict]],
    settings: provider_utils.Settings,
    **kwargs,
) -> typing.List[models.Message]:
    """Parse SmartKargo API error responses.

    Extracts errors from all SmartKargo response formats:
    - Plain text errors (e.g. 'Entity "Site" not found')
    - Error object: {"error": {"code": "...", "message": "..."}}
    - Top-level validations[]: {"validations": [{"message": "..."}]}
    - Nested shipments[].validations[]: rejected shipment errors
    - Status-based: {"status": "Rejected", "details": "..."}
    """
    responses = response if isinstance(response, list) else [response]

    return sum(
        [_extract_errors(res, settings, **kwargs) for res in responses],
        [],
    )


def _extract_errors(
    res: typing.Union[str, dict],
    settings: provider_utils.Settings,
    **kwargs,
) -> typing.List[models.Message]:
    """Extract all errors from a single response object."""

    # Plain text error (e.g. HTTP error body)
    if isinstance(res, str) and res.strip():
        return [_message(settings, "API_ERROR", res.strip(), **kwargs)]

    if not isinstance(res, dict):
        return []

    status = (res.get("status") or "").upper()
    valid = (res.get("valid") or "").upper()

    # Explicit error object: {"error": {"code": "...", "message": "..."}}
    error_obj = res.get("error")
    if isinstance(error_obj, dict):
        return [_message(
            settings,
            error_obj.get("code", "ERROR"),
            error_obj.get("message", "Unknown error"),
            **kwargs,
        )]

    # Successful response with no issues — skip
    if status in _SUCCESS_STATUSES and valid != "NO":
        top_validations = res.get("validations") or []
        if not top_validations:
            return []

    # Collect all errors from validations + shipments + status details
    top_validations = _parse_validations(res.get("validations"), settings, **kwargs)
    shipment_validations = _parse_shipment_validations(res.get("shipments"), settings, **kwargs)
    status_errors = _parse_status_error(res, settings, **kwargs)

    errors = [*top_validations, *shipment_validations, *status_errors]

    # Fallback: error status with no extractable details
    if status in _ERROR_STATUSES and not errors:
        return [_message(settings, "ERROR", "An unknown error occurred", **kwargs)]

    return errors


def _parse_validations(
    validations: typing.Optional[typing.List[dict]],
    settings: provider_utils.Settings,
    **kwargs,
) -> typing.List[models.Message]:
    """Parse top-level validations[] array."""
    return [
        _message(
            settings,
            v.get("property") or v.get("code", "VALIDATION_ERROR"),
            v.get("message", "Unknown validation error"),
            package_reference=v.get("packageReference"),
            **kwargs,
        )
        for v in (validations or [])
        if isinstance(v, dict)
    ]


def _parse_shipment_validations(
    shipments: typing.Optional[typing.List[dict]],
    settings: provider_utils.Settings,
    **kwargs,
) -> typing.List[models.Message]:
    """Parse nested shipments[].validations[] arrays."""
    return [
        _message(
            settings,
            v.get("code", "VALIDATION_ERROR"),
            v.get("message", "Unknown validation error"),
            package_reference=shipment.get("packageReference"),
            header_reference=shipment.get("headerReference"),
            shipment_status=(shipment.get("status") or "").upper() or None,
            **kwargs,
        )
        for shipment in (shipments or [])
        if isinstance(shipment, dict)
        for v in (shipment.get("validations") or [])
        if isinstance(v, dict)
    ]


def _parse_status_error(
    res: dict,
    settings: provider_utils.Settings,
    **kwargs,
) -> typing.List[models.Message]:
    """Parse status-based error with details string."""
    status = (res.get("status") or "").upper()
    details = res.get("details")

    if status in _ERROR_STATUSES and details:
        return [_message(settings, "API_ERROR", str(details), **kwargs)]

    return []


def _message(
    settings: provider_utils.Settings,
    code: str,
    message: str,
    **details,
) -> models.Message:
    """Build a Message with consistent carrier info and cleaned details."""
    return models.Message(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        code=code,
        message=message,
        details=lib.to_dict(details),
    )
