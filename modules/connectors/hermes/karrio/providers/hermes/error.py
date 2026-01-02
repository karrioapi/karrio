"""Karrio Hermes error parser."""

import typing
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.hermes.utils as provider_utils


def parse_error_response(
    response: typing.Union[dict, str, None],
    settings: provider_utils.Settings,
    **kwargs,
) -> typing.List[models.Message]:
    """Parse Hermes error response into karrio messages."""
    messages: typing.List[models.Message] = []

    if response is None:
        return messages

    # Handle case where response is not a dict (e.g., raw string response)
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

    # Handle OAuth2 error response
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

    # Handle Hermes API error response with listOfResultCodes
    result_codes = response.get("listOfResultCodes") or []
    for error in result_codes:
        code = error.get("code", "")
        message = error.get("message", "")

        # Only include actual errors (codes starting with 'e')
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
) -> typing.List[models.Message]:
    """Parse Hermes warning response into karrio messages."""
    messages: typing.List[models.Message] = []

    if response is None:
        return messages

    # Handle warnings from listOfResultCodes (codes starting with 'w')
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
