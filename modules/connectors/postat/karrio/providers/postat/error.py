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
    messages: typing.List[models.Message] = []

    # Extract SOAP faults (standard SOAP error handling)
    messages.extend(extract_fault(response, settings))

    # Parse PostAT errorMessage element (main error field in responses)
    error_messages = lib.find_element("errorMessage", response) or []
    for err_elem in error_messages:
        if err_elem.text and err_elem.text.strip():
            msg_text = err_elem.text.strip()
            # Avoid duplicates
            if not any(msg_text in (m.message or "") for m in messages):
                messages.append(
                    models.Message(
                        carrier_id=settings.carrier_id,
                        carrier_name=settings.carrier_name,
                        code="POSTAT_ERROR",
                        message=msg_text,
                        details=kwargs if kwargs else None,
                    )
                )

    return messages
