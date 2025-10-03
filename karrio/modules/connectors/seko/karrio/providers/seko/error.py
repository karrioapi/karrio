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
    errors: list = []

    for response_item in responses:
        if validation_errors := response_item.get("ValidationErrors"):
            if isinstance(validation_errors, dict):
                errors.append(
                    {
                        "code": "ValidationError",
                        "message": validation_errors.get(
                            "Message", next(iter(validation_errors.values()))
                        ),
                        **{
                            k: v for k, v in validation_errors.items() if k != "Message"
                        },
                    }
                )
            else:
                errors.append(
                    {"code": "ValidationError", "message": str(validation_errors)}
                )
            break

        if rejected := response_item.get("Rejected", []):
            error = rejected[0]
            errors.append(
                {
                    "code": "Rejected",
                    "message": error.get("Reason"),
                    **{k: v for k, v in error.items() if k != "Reason"},
                }
            )
            break

        if general_errors := (
            response_item.get("Errors", []) or response_item.get("Error", [])
        ):
            error = general_errors[0]
            errors.append(
                {
                    "code": "Error",
                    "message": error.get("Message"),
                    **{k: v for k, v in error.items() if k != "Message"},
                }
            )
            break

    return [
        models.Message(
            carrier_id=settings.carrier_id,
            carrier_name=settings.carrier_name,
            code=error["code"],
            message=error["message"],
            details={
                **kwargs,
                **{k: v for k, v in error.items() if k not in ["code", "message"]},
            },
        )
        for error in errors
    ]
