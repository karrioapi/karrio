import laposte_lib.error as laposte
import typing
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.laposte.utils as provider_utils


def parse_error_response(
    response: typing.Union[dict, typing.List[dict]],
    settings: provider_utils.Settings,
    **kwargs,
) -> typing.List[models.Message]:
    responses = response if isinstance(response, list) else [response]
    errors = [
        lib.to_object(laposte.Error, res)
        for res in responses
        if not str(res.get("returnCode")).startswith("20")
    ]

    return [
        models.Message(
            carrier_id=settings.carrier_id,
            carrier_name=settings.carrier_name,
            code=error.returnCode,
            message=error.returnMessage,
            details={**kwargs},
        )
        for error in errors
    ]
