"""Karrio Asendia error parser."""

import typing
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.asendia.utils as provider_utils
import karrio.schemas.asendia.error_response as asendia


def parse_error_response(
    response: dict,
    settings: provider_utils.Settings,
    **kwargs,
) -> typing.List[models.Message]:
    """Parse Asendia error response into karrio Message objects.

    Asendia error format:
    {
        "type": "https://www.asendia-sync.com/problem/constraint-violation",
        "title": "Bad Request",
        "status": 400,
        "detail": "Validation failed",
        "path": "/api/parcels",
        "message": "error.validation",
        "fieldErrors": [{"objectName": "...", "field": "...", "message": "..."}]
    }
    """
    errors: typing.List[models.Message] = []

    # Check if response contains error indicators
    if response is None:
        return errors

    # Get status code from response - must be a numeric value (HTTP status code)
    # Non-numeric status values (like "CREATED" in manifest responses) are not error codes
    raw_status = response.get("status")
    status_code = None
    if raw_status is not None and isinstance(raw_status, (int, float)):
        status_code = int(raw_status)
    elif raw_status is not None and isinstance(raw_status, str):
        try:
            status_code = int(raw_status)
        except ValueError:
            # Not a numeric status code (e.g., "CREATED"), not an error
            status_code = None

    # Parse error response using generated schema (only if there's an error indicator)
    error = lib.to_object(asendia.ErrorResponseType, response)

    # Check for error status or error fields
    is_error = (
        (status_code is not None and status_code >= 400)
        or error.title is not None
        or (error.fieldErrors is not None and len(error.fieldErrors) > 0)
    )

    if not is_error:
        return errors

    # If there are field-level errors, create a message for each
    if error.fieldErrors:
        for field_error in error.fieldErrors:
            errors.append(
                models.Message(
                    carrier_id=settings.carrier_id,
                    carrier_name=settings.carrier_name,
                    code=str(status_code or "ERROR"),
                    message=f"{field_error.field}: {field_error.message}",
                    details={
                        "objectName": field_error.objectName,
                        "field": field_error.field,
                        **kwargs,
                    },
                )
            )
    else:
        # General error without field-specific details
        errors.append(
            models.Message(
                carrier_id=settings.carrier_id,
                carrier_name=settings.carrier_name,
                code=str(status_code or "ERROR"),
                message=error.detail or error.message or error.title or "Unknown error",
                details={
                    "type": error.type,
                    "path": error.path,
                    **kwargs,
                },
            )
        )

    return errors
