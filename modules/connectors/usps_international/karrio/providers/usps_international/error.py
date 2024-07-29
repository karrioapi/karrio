"""Karrio USPS error parser."""

import typing
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.usps_international.utils as provider_utils


def parse_error_response(
    response: typing.Union[dict, typing.List[dict]],
    settings: provider_utils.Settings,
    **kwargs,
) -> typing.List[models.Message]:
    responses = response if isinstance(response, list) else [response]
    errors: list = [response["error"] for response in responses if "error" in response]

    return [
        models.Message(
            carrier_id=settings.carrier_id,
            carrier_name=settings.carrier_name,
            code=error.get("code"),
            message=error.get("message"),
            details={**kwargs, "errors": error.get("errors", [])},
        )
        for error in errors
    ]
