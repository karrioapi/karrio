import karrio.schemas.boxknight.error as boxknight
import typing
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.boxknight.utils as provider_utils


def parse_error_response(
    response: typing.Union[dict, typing.List[dict]],
    settings: provider_utils.Settings,
    **kwargs,
) -> typing.List[models.Message]:
    responses = response if isinstance(response, list) else [response]
    errors = [
        lib.to_object(boxknight.Error, res)
        for res in responses
        if res.get("error") is not None
    ]

    return [
        models.Message(
            carrier_id=settings.carrier_id,
            carrier_name=settings.carrier_name,
            code=None,
            message=error.error,
            details={**kwargs},
        )
        for error in errors
    ]
