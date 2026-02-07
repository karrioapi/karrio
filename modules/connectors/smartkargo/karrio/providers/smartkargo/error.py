"""Karrio SmartKargo error parser."""

import typing
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.smartkargo.utils as provider_utils


def parse_error_response(
    response: typing.Union[dict, typing.List[dict]],
    settings: provider_utils.Settings,
    **kwargs,
) -> typing.List[models.Message]:
    """Parse SmartKargo API error response.

    SmartKargo errors come in several formats per API manual (Pages 11-12, 20-24):
    1. Validation errors: {"status": "Rejected", "validations": [{"property": "...", "message": "...", "packageReference": "..."}]}
    2. Error object: {"error": {"code": "...", "message": "..."}}
    3. Status-based: {"status": "Error/Failed/Rejected", "details": "..."}
    """
    responses = response if isinstance(response, list) else [response]
    errors: typing.List[models.Message] = []

    for res in responses:
        if not isinstance(res, dict):
            continue

        status = res.get("status", "")
        valid = res.get("valid", "")

        # Check for explicit error object
        error_obj = res.get("error")
        if error_obj and isinstance(error_obj, dict):
            errors.append(
                models.Message(
                    carrier_id=settings.carrier_id,
                    carrier_name=settings.carrier_name,
                    code=error_obj.get("code", "ERROR"),
                    message=error_obj.get("message", "Unknown error"),
                    details={**kwargs},
                )
            )
            continue

        # Skip successful responses
        if status.upper() in ["PROCESSED", "QUOTED", "SUCCESS", "OK", ""] and valid.upper() != "NO":
            # Check for validation warnings in successful responses
            validations = res.get("validations") or []
            if not validations:
                continue

        # Extract validation errors
        validations = res.get("validations") or []
        for validation in validations:
            if isinstance(validation, dict):
                errors.append(
                    models.Message(
                        carrier_id=settings.carrier_id,
                        carrier_name=settings.carrier_name,
                        code=validation.get("property") or validation.get("code", "VALIDATION_ERROR"),
                        message=validation.get("message", "Unknown validation error"),
                        details={
                            "package_reference": validation.get("packageReference"),
                            **kwargs,
                        },
                    )
                )

        # Extract general error details
        details = res.get("details")
        if details and status.upper() in ["ERROR", "FAILED", "REJECTED"]:
            errors.append(
                models.Message(
                    carrier_id=settings.carrier_id,
                    carrier_name=settings.carrier_name,
                    code="API_ERROR",
                    message=str(details) if details else "Unknown API error",
                    details={**kwargs},
                )
            )

        # Handle case where there's an error status but no details
        if status.upper() in ["ERROR", "FAILED", "REJECTED"] and not validations and not details and not error_obj:
            errors.append(
                models.Message(
                    carrier_id=settings.carrier_id,
                    carrier_name=settings.carrier_name,
                    code="ERROR",
                    message="An unknown error occurred",
                    details={**kwargs},
                )
            )

    return errors
