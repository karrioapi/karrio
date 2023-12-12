import typing
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.easypost.utils as provider_utils


def parse_error_response(
    response: dict, settings: provider_utils.Settings, **kwargs
) -> typing.List[models.Message]:
    errors = [
        *response.get("messages", []),
        *([response.get("error")] if "error" in response else []),
    ]

    return [
        models.Message(
            carrier_id=settings.carrier_id,
            carrier_name=settings.carrier_name,
            code=(error.get("code") or error.get("type")),
            message=error.get("message"),
            details=lib.to_dict(
                {
                    "errors": error.get("errors"),
                    "carrier": error.get("carrier"),
                    "carrier_account_id": error.get("carrier_account_id"),
                    **kwargs,
                }
            ),
        )
        for error in errors
    ]
