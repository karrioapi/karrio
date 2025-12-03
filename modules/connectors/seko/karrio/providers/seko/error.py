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
                        "level": (validation_errors.get("Severity") or "error").lower(),
                        **{
                            k: v for k, v in validation_errors.items() if k not in ["Message", "Severity"]
                        },
                    }
                )
            elif isinstance(validation_errors, list):
                for ve in validation_errors:
                    errors.append(
                        {
                            "code": ve.get("ErrorCode") or "ValidationError",
                            "message": ve.get("Message"),
                            "level": (ve.get("Severity") or "error").lower(),
                            **{
                                k: v for k, v in ve.items() if k not in ["Message", "Severity", "ErrorCode"]
                            },
                        }
                    )
            else:
                errors.append(
                    {"code": "ValidationError", "message": str(validation_errors), "level": "error"}
                )
            break

        if rejected := response_item.get("Rejected", []):
            error = rejected[0]
            errors.append(
                {
                    "code": "Rejected",
                    "message": error.get("Reason"),
                    "level": "error",
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
                    "level": (error.get("Severity") or "error").lower(),
                    **{k: v for k, v in error.items() if k not in ["Message", "Severity"]},
                }
            )
            break

        # Handle Warnings array
        if warnings := response_item.get("Warnings", []):
            for warning in warnings:
                errors.append(
                    {
                        "code": warning.get("WarningCode") or warning.get("ErrorCode") or "Warning",
                        "message": warning.get("Message"),
                        "level": (warning.get("Severity") or "warning").lower(),
                        **{
                            k: v for k, v in warning.items() if k not in ["Message", "Severity", "WarningCode", "ErrorCode"]
                        },
                    }
                )

    return [
        models.Message(
            carrier_id=settings.carrier_id,
            carrier_name=settings.carrier_name,
            code=error["code"],
            message=error["message"],
            level=error.get("level"),
            details={
                **kwargs,
                **{k: v for k, v in error.items() if k not in ["code", "message", "level"]},
            },
        )
        for error in errors
    ]
