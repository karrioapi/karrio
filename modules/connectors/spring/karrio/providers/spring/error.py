"""Karrio Spring error parser."""

import typing
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.spring.utils as provider_utils


def parse_error_response(
    response: dict,
    settings: provider_utils.Settings,
    **kwargs,
) -> typing.List[models.Message]:
    """Parse Spring API error response.

    Spring API uses ErrorLevel codes:
    - 0: Command successfully completed without any errors
    - 1: Command completed with errors (e.g., shipment created with errors)
    - 10: Fatal error, command is not completed at all
    """
    errors: typing.List[models.Message] = []

    if not isinstance(response, dict):
        return errors

    error_level = response.get("ErrorLevel")
    error_message = response.get("Error") or ""

    # ErrorLevel 0 means success, no errors
    if error_level == 0:
        return errors

    # ErrorLevel 1 or 10 indicates an error
    if error_level in (1, 10):
        errors.append(
            models.Message(
                carrier_id=settings.carrier_id,
                carrier_name=settings.carrier_name,
                code=str(error_level),
                message=error_message or (
                    "Command completed with errors" if error_level == 1
                    else "Fatal error, command not completed"
                ),
                details={**kwargs},
            )
        )

    return errors
