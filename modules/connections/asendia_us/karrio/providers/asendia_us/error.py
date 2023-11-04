import typing
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.asendia_us.utils as provider_utils


def parse_error_response(
    response: dict,
    settings: provider_utils.Settings,
    **kwargs,
) -> typing.List[models.Message]:
    responses = response if isinstance(response, list) else [response]
    errors = [
        error.get("responseStatus") or error
        for error in responses
        if (
            error.get("responseStatusCode") is not None
            or error.get("responseStatus") is not None
        )
    ]

    return [
        models.Message(
            carrier_id=settings.carrier_id,
            carrier_name=settings.carrier_name,
            code=error.get("responseStatusCode"),
            message=error.get("responseStatusMessage"),
            details={**kwargs},
        )
        for error in errors
    ]
