import typing
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.hay_post.utils as provider_utils

import karrio.schemas.hay_post.error as hay_post


def parse_error_response(
    response: dict,
    settings: provider_utils.Settings,
    **kwargs,
) -> typing.List[models.Message]:
    responses = response if isinstance(response, list) else [response]

    errors: typing.List[hay_post.ErrorType] = [
        lib.to_object(hay_post.ErrorType, error) for error in responses
    ]

    return [
        models.Message(
            carrier_id=settings.carrier_id,
            carrier_name=settings.carrier_name,
            code="error",
            message=" ".join(error.key.split("_")).capitalize(),
            details={**kwargs},
        )
        for error in errors
        if error.key is not None
    ]
