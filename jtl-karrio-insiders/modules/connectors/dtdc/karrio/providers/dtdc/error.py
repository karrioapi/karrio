"""Karrio DTDC error parser."""

import typing
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.dtdc.utils as provider_utils
import karrio.schemas.dtdc.error_response as dtdc_res


def parse_error_response(
    response: typing.Union[typing.List[dict], dict],
    settings: provider_utils.Settings,
    **details,
) -> typing.List[models.Message]:
    responses = response if isinstance(response, list) else [response]
    errors: typing.List[dict] = [
        dict(
            code=lib.identity(
                lib.failsafe(lambda: response["error"]["reason"])
                or lib.failsafe(lambda: response["data"][0]["reason"])
                or lib.failsafe(lambda: response["status"])
            ),
            message=lib.identity(
                response.get("message")
                or response.get("reason")
                or lib.failsafe(lambda: response["error"]["message"])
                or lib.failsafe(lambda: response["data"][0]["message"])
            ),
            details=lib.identity(
                lib.failsafe(lambda: response.get("errorDetails"))
                or lib.failsafe(lambda: response.get("error"))
                or lib.failsafe(lambda: response.get("data"))
                or response
            ),
        )
        for response in responses
        if (
            response.get("message")
            or response.get("error")
            or response.get("errorDetails")
            or (response.get("code") and response.get("reason"))
            or lib.failsafe(
                lambda: (
                    response["data"][0]["success"] == False
                    and response["data"][0]["message"]
                )
            )
        )
    ]

    return [
        models.Message(
            carrier_name=settings.carrier_name,
            carrier_id=settings.carrier_id,
            code=error.get("code"),
            message=error.get("message"),
            details=lib.to_dict(
                {
                    **details,
                    "tracking_number": error.get("tracking_number"),
                }
            ),
        )
        for error in errors
    ]
