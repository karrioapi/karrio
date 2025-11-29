"""Karrio GLS Group error parser."""

import typing
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.gls_group.utils as provider_utils
import karrio.schemas.gls_group.error_response as gls_error


def parse_error_response(
    response: dict,
    settings: provider_utils.Settings,
    **kwargs,
) -> typing.List[models.Message]:
    """Parse GLS Group error response."""
    errors = response.get("errors", []) if isinstance(response, dict) else []

    return [
        models.Message(
            carrier_id=settings.carrier_id,
            carrier_name=settings.carrier_name,
            code=lib.text(error.get("code", "")),
            message=lib.text(error.get("message", "")),
            details={
                **kwargs,
                "field": error.get("field"),
                "details": error.get("details"),
            },
        )
        for error in errors
    ]
