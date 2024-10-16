"""Karrio Easyship error parser."""

import typing
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.easyship.utils as provider_utils


def parse_error_response(
    response: dict,
    settings: provider_utils.Settings,
    **kwargs,
) -> typing.List[models.Message]:
    errors: list = [
        *([response["error"]] if response.get("error") else []),
        *[
            dict(code="warning", message=message)
            for message in response.get("meta", {}).get("errors", [])
        ],
    ]

    return [
        models.Message(
            carrier_id=settings.carrier_id,
            carrier_name=settings.carrier_name,
            code=error.get("code"),
            message=error.get("message"),
            details=lib.to_dict(
                {
                    **kwargs,
                    "details": error.get("details"),
                    "request_id": error.get("request_id"),
                    "type": error.get("type"),
                }
            ),
        )
        for error in errors
    ]
