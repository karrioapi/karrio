"""Karrio SEKO Logistics error parser."""

import typing
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.seko.utils as provider_utils


def parse_error_response(
    response: typing.Union[typing.List[dict], dict],
    settings: provider_utils.Settings,
    **kwargs,
) -> typing.List[models.Message]:
    responses = response if isinstance(response, list) else [response]
    errors: list = sum(
        [
            [
                *lib.identity(
                    [
                        {"code": "Error", "message": e.get("Message"), **e}
                        for e in _.get("Errors", [])
                    ]
                    if any(_.get("Errors", []))
                    else []
                ),
                *lib.identity(
                    [
                        {"code": "Error", "message": e.get("Message"), **e}
                        for e in _.get("Error", [])
                    ]
                    if any(_.get("Error", []))
                    else []
                ),
                *lib.identity(
                    [
                        {"code": "Rejected", "message": e.get("Reason"), **e}
                        for e in _.get("Error", [])
                    ]
                    if any(_.get("Rejected", []))
                    else []
                ),
                *lib.identity(
                    [
                        {"code": "ValidationError", "message": e.get("Message"), **e}
                        for e in [_.get("ValidationErrors")]
                    ]
                    if _.get("ValidationErrors")
                    else []
                ),
            ]
            for _ in responses
        ],
        [],
    )

    return [
        models.Message(
            carrier_id=settings.carrier_id,
            carrier_name=settings.carrier_name,
            code=error["code"],
            message=error["message"],
            details={
                **kwargs,
                **{
                    k: v
                    for k, v in error.items()
                    if k not in ["code", "message", "Code", "Message"]
                },
            },
        )
        for error in errors
    ]
