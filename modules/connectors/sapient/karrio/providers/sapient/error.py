"""Karrio SAPIENT error parser."""

import typing
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.sapient.utils as provider_utils


def parse_error_response(
    response: typing.Union[dict, typing.List[dict]],
    settings: provider_utils.Settings,
    **kwargs,
) -> typing.List[models.Message]:
    responses = response if isinstance(response, list) else [response]
    errors: typing.List[dict] = sum(
        [_["Errors"] for _ in responses if "Errors" in _], []
    )

    return [
        models.Message(
            carrier_id=settings.carrier_id,
            carrier_name=settings.carrier_name,
            code=error.get("ErrorCode", "UNKNOWN"),
            message=error.get("Message", "Unknown error"),
            details=lib.to_dict({**kwargs, "Cause": error.get("Cause")}),
        )
        for error in errors
    ]
