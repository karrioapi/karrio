"""Karrio DPD Group error parser."""

import typing
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.dpd_group.utils as provider_utils
import karrio.schemas.dpd_group.error_response as dpd_error


def parse_error_response(
    response: typing.Union[dict, typing.Any],
    settings: provider_utils.Settings,
    **kwargs,
) -> typing.List[models.Message]:
    """Parse DPD META-API error response."""
    errors = []

    # Handle dict response
    if isinstance(response, dict):
        # Check for DPD error format
        if "errorCode" in response or "errorMessage" in response:
            error = lib.to_object(dpd_error.ErrorResponseType, response)
            errors.append(
                models.Message(
                    carrier_id=settings.carrier_id,
                    carrier_name=settings.carrier_name,
                    code=error.errorCode or "ERROR",
                    message=error.errorMessage or "Unknown error",
                    details={
                        **kwargs,
                        "errorOrigin": error.errorOrigin,
                    },
                )
            )
        # Check for HTTP error response
        elif response.get("detail"):
            errors.append(
                models.Message(
                    carrier_id=settings.carrier_id,
                    carrier_name=settings.carrier_name,
                    code="HTTP_ERROR",
                    message=response.get("detail"),
                    details=kwargs,
                )
            )

    return errors
