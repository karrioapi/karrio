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

    # Parse error response using generated schema
    error = lib.to_object(asendia.ErrorResponseType, response)

    # Check for error status or error fields
    is_error = (
        (error.status is not None and error.status >= 400)
        or error.title is not None
        or error.message is not None
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
                    code=str(error.status or "ERROR"),
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
                code=str(error.status or "ERROR"),
                message=error.detail or error.message or error.title or "Unknown error",
                details={
                    "type": error.type,
                    "path": error.path,
                    **kwargs,
                },
            )
        )

    return errors
