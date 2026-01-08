"""Karrio GLS Group error parser."""

import typing
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.gls.utils as provider_utils
import karrio.schemas.gls.error_response as gls_error


def parse_error_response(
    response: dict,
    settings: provider_utils.Settings,
    **kwargs,
) -> typing.List[models.Message]:
    """Parse GLS Group error response."""
    if not isinstance(response, dict):
        return []
    
    # Convert to typed object using generated schema
    error_response = lib.to_object(gls_error.ErrorResponseType, response)

    return [
        models.Message(
            carrier_id=settings.carrier_id,
            carrier_name=settings.carrier_name,
            code=lib.text(error.code or ""),
            message=lib.text(error.message or ""),
            details={
                **kwargs,
                "field": error.field,
                "details": error.details,
            },
        )
        for error in (error_response.errors or [])
    ]
