"""Karrio PostAT error parser."""

import karrio.core.models as models
import karrio.lib as lib
import karrio.providers.postat.utils as provider_utils
from karrio.core.utils.soap import extract_fault


def parse_error_response(
    response: lib.Element,
    settings: provider_utils.Settings,
    **kwargs,
) -> list[models.Message]:
    """Parse error response from PostAT SOAP API."""
    messages: list[models.Message] = []

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
