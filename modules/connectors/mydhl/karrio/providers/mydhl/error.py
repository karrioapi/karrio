"""Karrio DHL Express error parser."""

import typing
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.mydhl.utils as provider_utils


def parse_error_response(
    response: typing.Union[dict, typing.List[dict]],
    settings: provider_utils.Settings,
    **kwargs,
) -> typing.List[models.Message]:
    responses = response if isinstance(response, list) else [response]
    errors: list = [
        *[_ for _ in responses if _.get("title") is not None],
        *sum(
            [
                [dict(code="warning", message=_) for _ in __.get("warnings")]
                for __ in responses
                if __.get("warnings")
            ],
            [],
        ),
    ]

    return [
        models.Message(
            carrier_id=settings.carrier_id,
            carrier_name=settings.carrier_name,
            code=error.get("status"),
            message=error.get("title") or error.get("message"),
            details={
                **kwargs,
                "detail": error.get("detail"),
                "instance": error.get("instance"),
            },
        )
        for error in errors
    ]
