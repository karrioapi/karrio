"""Karrio Hermes error parser."""

import karrio.core.models as models
import karrio.providers.hermes.utils as provider_utils


def parse_error_response(
    response: dict | str | None,
    settings: provider_utils.Settings,
    **kwargs,
) -> list[models.Message]:
    """Parse Hermes error response into karrio messages. See SPECS.md (Errors)."""
    messages: list[models.Message] = []

    if response is None:
        return messages

    if not isinstance(response, dict):
        messages.append(
            models.Message(
                carrier_id=settings.carrier_id,
                carrier_name=settings.carrier_name,
                code="PARSE_ERROR",
                message=f"Unexpected response format: {str(response)[:200]}",
                details={**kwargs},
            )
        )
        return messages

    if "error" in response:
        messages.append(
            models.Message(
                carrier_id=settings.carrier_id,
                carrier_name=settings.carrier_name,
                code=response.get("error", "AUTH_ERROR"),
                message=response.get("error_description", "Authentication failed"),
                details={**kwargs},
            )
        )

    result_codes = response.get("listOfResultCodes") or []
    for error in result_codes:
        code = error.get("code", "")
        message = error.get("message", "")

        if code.startswith("e") or (code and not code.startswith("w")):
            messages.append(
                models.Message(
                    carrier_id=settings.carrier_id,
                    carrier_name=settings.carrier_name,
                    code=code,
                    message=message,
                    details={**kwargs},
                )
            )

    return messages


def parse_warning_response(
    response: dict,
    settings: provider_utils.Settings,
    **kwargs,
) -> list[models.Message]:
    """Parse Hermes warning response into karrio messages."""
    messages: list[models.Message] = []

    if response is None:
        return messages

    result_codes = response.get("listOfResultCodes") or []
    for warning in result_codes:
        code = warning.get("code", "")
        message = warning.get("message", "")

        if code.startswith("w"):
            messages.append(
                models.Message(
                    carrier_id=settings.carrier_id,
                    carrier_name=settings.carrier_name,
                    code=code,
                    message=message,
                    details={**kwargs},
                )
            )

    return messages
