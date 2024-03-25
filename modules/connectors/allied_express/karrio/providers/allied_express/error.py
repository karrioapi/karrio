import typing
import karrio.core.models as models
import karrio.providers.allied_express.utils as provider_utils


def parse_error_response(
    response: provider_utils.AlliedResponse,
    settings: provider_utils.Settings,
    **kwargs,
) -> typing.List[models.Message]:
    errors = []

    if response.error is not None:
        errors.append(["500", response.error])

    if response.is_error and response.data is not None:
        errors.append(
            [
                "400",
                response.data["result"].get("statusError")
                or response.data["result"].get("errors"),
            ]
        )

    return [
        models.Message(
            carrier_id=settings.carrier_id,
            carrier_name=settings.carrier_name,
            code=code,
            message=message,
            details={**kwargs},
        )
        for code, message in errors
    ]
