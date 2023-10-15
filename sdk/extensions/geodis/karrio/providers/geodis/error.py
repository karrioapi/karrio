import karrio.schemas.geodis.error_response as geodis
import typing
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.geodis.utils as provider_utils


def parse_error_response(
    response: typing.Union[dict, typing.List[dict]],
    settings: provider_utils.Settings,
    **kwargs,
) -> typing.List[models.Message]:
    responses = response if isinstance(response, list) else [response]
    errors = [
        lib.to_object(geodis.ErrorResponseType, res)
        for res in responses
        if res.get("ok") is False
    ]

    return [
        models.Message(
            carrier_id=settings.carrier_id,
            carrier_name=settings.carrier_name,
            code=error.codeErreur,
            message=error.texteErreur,
            details={**kwargs},
        )
        for error in errors
    ]
