"""Karrio ParcelOne error parser."""

import typing
import karrio.lib as lib
import karrio.core.models as models
from karrio.core.utils.soap import extract_fault
import karrio.providers.parcelone.utils as provider_utils


def parse_error_response(
    response: lib.Element,
    settings: provider_utils.Settings,
    **kwargs,
) -> typing.List[models.Message]:
    """Parse error response from ParcelOne SOAP API."""
    errors = lib.find_element("Error", response) or []

    return [
        models.Message(
            carrier_id=settings.carrier_id,
            carrier_name=settings.carrier_name,
            code=_get_text("ErrorNo", error) or _get_text("StatusCode", error),
            message=_get_text("Message", error),
            details=kwargs or None,
        )
        for error in errors
        if _get_text("ErrorNo", error) or _get_text("Message", error)
    ] + extract_fault(response, settings)


def _get_text(name: str, element: lib.Element) -> typing.Optional[str]:
    """Get text from a namespace-qualified element."""
    found = lib.find_element(name, element, first=True)
    return found.text if found is not None else None
