"""Karrio PostAT error parser."""

import typing
import karrio.lib as lib
import karrio.core.models as models
from karrio.core.utils.soap import extract_fault
import karrio.providers.postat.utils as provider_utils


def parse_error_response(
    response: lib.Element,
    settings: provider_utils.Settings,
    **kwargs,
) -> typing.List[models.Message]:
    """Parse error response from PostAT SOAP API."""
    errors = lib.find_element("Error", response) or []

    return [
        models.Message(
            carrier_id=settings.carrier_id,
            carrier_name=settings.carrier_name,
            code=error.findtext("Code") or "ERROR",
            message=error.findtext("Message") or "",
            details={
                **({"description": error.findtext("Description")} if error.findtext("Description") else {}),
                **kwargs,
            },
        )
        for error in errors
    ] + extract_fault(response, settings)
