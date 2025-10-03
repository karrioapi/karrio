"""Karrio USPS error parser."""

import typing
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.usps.utils as provider_utils


def parse_error_response(
    response: typing.Union[dict, typing.List[dict]],
    settings: provider_utils.Settings,
    **kwargs,
) -> typing.List[models.Message]:
    responses = response if isinstance(response, list) else [response]
    errors = [
        *(
            [response]
            if isinstance(response, dict)
            and isinstance(response.get("error"), dict)
            and not any(response.get("error").get("errors") or [])
            else []
        ),
        *(
            [response]
            if isinstance(response, dict) and isinstance(response.get("error"), str)
            else []
        ),
        *(
            response["error"]["errors"]
            if isinstance(response, dict)
            and isinstance(response.get("error"), dict)
            and response.get("error").get("errors")
            else []
        ),
    ]

    return [
        models.Message(
            carrier_id=settings.carrier_id,
            carrier_name=settings.carrier_name,
            code=lib.identity(error.get("code") or error.get("error")),
            message=lib.identity(
                error.get("message")
                or error.get("detail")
                or error.get("error_description", "")
            ),
            details=lib.to_dict(
                {
                    **kwargs,
                    "source": error.get("source"),
                    "error_uri": error.get("error_uri"),
                }
            ),
        )
        for error in errors
    ]
