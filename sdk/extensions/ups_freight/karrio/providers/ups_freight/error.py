import typing
import karrio.core.models as models
import karrio.providers.ups_freight.utils as provider_utils


def parse_error_response(
    errors: typing.Union[typing.List[dict], dict],
    settings: provider_utils.Settings,
    details: dict = None,
) -> typing.List[models.Message]:
    errors = errors if isinstance(errors, list) else [errors]

    return [
        models.Message(
            carrier_name=settings.carrier_name,
            carrier_id=settings.carrier_id,
            code=error.get("code") or error.get("Code"),
            message=error.get("message") or error.get("Description"),
            details=details,
        )
        for error in errors
    ]
