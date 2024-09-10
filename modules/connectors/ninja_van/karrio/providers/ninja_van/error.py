"""Karrio Ninja Van error parser."""
import typing
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.ninja_van.utils as provider_utils


def parse_error_response(
    response: typing.Union[typing.List[dict], dict],
    settings: provider_utils.Settings,
    **details,
) -> typing.List[models.Message]:
    responses = response if isinstance(response, list) else [response]
    errors: typing.List[dict] = sum(
        [
            result["error"]["details"]
            if "error" in result and "details" in result["error"]
            else []
            for result in responses
        ],
        [],
    )

    messages: typing.List[models.Message] = [
        models.Message(
            carrier_name=settings.carrier_name,
            carrier_id=settings.carrier_id,
            code=error.get("reason"),
            message=error.get("message"),
            details=details,
        )
        for error in errors
    ]

    return messages
