"""Karrio Amazon Shipping error parser."""

import karrio.core.models as models
import karrio.providers.amazon_shipping.utils as provider_utils


def parse_error_response(
    response: dict,
    settings: provider_utils.Settings,
    **kwargs,
) -> list[models.Message]:
    """Parse the v2 ``{"errors": [...]}`` envelope into messages. See SPECS.md."""
    errors = response.get("errors") or []

    return [
        models.Message(
            carrier_id=settings.carrier_id,
            carrier_name=settings.carrier_name,
            code=error.get("code"),
            message=error.get("message"),
            details={
                **kwargs,
                **({"note": error.get("details")} if error.get("details") else {}),
            }
            or None,
        )
        for error in errors
        if error.get("code") or error.get("message")
    ]
