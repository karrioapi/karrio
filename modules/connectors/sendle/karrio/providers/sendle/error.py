import karrio.schemas.sendle.error_responses as sendle
import typing
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.sendle.utils as provider_utils


def parse_error_response(
    response: typing.Union[typing.List[dict], dict],
    settings: provider_utils.Settings,
    **kwargs,
) -> typing.List[models.Message]:
    responses = response if isinstance(response, list) else [response]
    errors: typing.List[sendle.ErrorResponseType] = [
        lib.to_object(sendle.ErrorResponseType, error)
        for error in responses
        if isinstance(error, dict) and error.get("error") is not None
    ]

    return [
        models.Message(
            carrier_id=settings.carrier_id,
            carrier_name=settings.carrier_name,
            code=error.error,
            message=(
                error.messages
                if isinstance(error.messages, str)
                else error.error_description
            ).strip(),
            details={
                **kwargs,
                "messages": error.messages,
                "error_description": error.error_description.strip(),
            },
        )
        for error in errors
    ]
