import karrio.schemas.colissimo.error_response as laposte
import typing
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.colissimo.utils as provider_utils


def parse_error_response(
    response: dict,
    settings: provider_utils.Settings,
    **kwargs,
) -> typing.List[models.Message]:
    messages = response.get("json_info", {}).get("messages", [])

    return [
        models.Message(
            carrier_id=settings.carrier_id,
            carrier_name=settings.carrier_name,
            code=msg.get("type"),
            message=msg.get("messageContent"),
            details={**kwargs},
        )
        for msg in messages
        if msg.get("type") == "ERROR"
    ]


def parse_laposte_error_response(
    response: typing.Union[dict, typing.List[dict]],
    settings: provider_utils.Settings,
    **kwargs,
) -> typing.List[models.Message]:
    responses = response if isinstance(response, list) else [response]
    errors = [
        lib.to_object(laposte.ErrorResponse, res)
        for res in responses
        if (
            not str(res.get("returnCode")).startswith("20")
            or res.get("code") is not None
        )
    ]

    return [
        models.Message(
            carrier_id=settings.carrier_id,
            carrier_name=settings.carrier_name,
            code=(error.returnCode or error.code),
            message=(error.returnMessage or error.message),
            details={**kwargs},
        )
        for error in errors
    ]
