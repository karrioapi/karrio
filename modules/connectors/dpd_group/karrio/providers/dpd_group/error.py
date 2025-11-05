"""Karrio DPD Group error parser."""

import typing
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.dpd_group.utils as provider_utils
import karrio.schemas.dpd_group.error_response as dpd_group


def parse_error_response(
    response: typing.Union[dict, str],
    settings: provider_utils.Settings,
    **kwargs,
) -> typing.List[models.Message]:
    """Parse DPD Group error response."""
    errors = []

    # Handle string responses (might be empty or non-JSON)
    if isinstance(response, str):
        if not response.strip():
            return []
        try:
            response = lib.to_dict(response)
        except:
            return [
                models.Message(
                    carrier_id=settings.carrier_id,
                    carrier_name=settings.carrier_name,
                    code="ERROR",
                    message=response,
                )
            ]

    # Parse error response
    if not isinstance(response, dict):
        return []

    error_data = response.get("error")
    if not error_data:
        # Check if the response itself indicates an error
        if response.get("status", 200) >= 400:
            return [
                models.Message(
                    carrier_id=settings.carrier_id,
                    carrier_name=settings.carrier_name,
                    code=str(response.get("status", "ERROR")),
                    message=response.get("message", "An error occurred"),
                )
            ]
        return []

    try:
        error = lib.to_object(dpd_group.ErrorResponseType, response)

        # Main error message
        errors.append(
            models.Message(
                carrier_id=settings.carrier_id,
                carrier_name=settings.carrier_name,
                code=error.error.code if hasattr(error.error, 'code') else "ERROR",
                message=error.error.message if hasattr(error.error, 'message') else "An error occurred",
                details=lib.to_dict(error.error.details) if hasattr(error.error, 'details') and error.error.details else {}
            )
        )

        # Additional detail messages
        if hasattr(error.error, 'details') and error.error.details:
            for detail in error.error.details:
                if hasattr(detail, 'field') and hasattr(detail, 'message'):
                    errors.append(
                        models.Message(
                            carrier_id=settings.carrier_id,
                            carrier_name=settings.carrier_name,
                            code="VALIDATION_ERROR",
                            message=f"{detail.field}: {detail.message}",
                        )
                    )
    except Exception as e:
        errors.append(
            models.Message(
                carrier_id=settings.carrier_id,
                carrier_name=settings.carrier_name,
                code="PARSE_ERROR",
                message=str(e),
            )
        )

    return errors
