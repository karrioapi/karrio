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

    SmartKargo errors come in two formats:
    1. Validation errors: {"status": "ERROR", "validations": [{"property": "...", "message": "..."}]}
    2. General errors: {"status": "ERROR", "details": "..."}
    """
    responses = response if isinstance(response, list) else [response]
    errors: typing.List[models.Message] = []

    for res in responses:
        if not isinstance(res, dict):
            continue

        status = res.get("status", "")

        # Skip successful responses
        if status.upper() in ["OK", "SUCCESS", ""]:
            # Check for validation errors in successful responses (warnings)
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
                        code=validation.get("property", "VALIDATION_ERROR"),
                        message=validation.get("message", "Unknown validation error"),
                        details={
                            "package_reference": validation.get("packageReference"),
                            **kwargs,
                        },
                    )
                )

        # Extract general error details
        details = res.get("details")
        if details and status.upper() == "ERROR":
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
        if status.upper() == "ERROR" and not validations and not details:
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
