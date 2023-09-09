import typing
import urllib.error
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.locate2u.utils as provider_utils


def parse_error_response(
    responses: typing.Union[typing.List[dict], dict],
    settings: provider_utils.Settings,
    **kwargs,
) -> typing.List[models.Message]:
    results = responses if isinstance(responses, list) else [responses]
    errors: typing.List[dict] = [
        error for error in results if error.get("error") is not None
    ]

    return [
        models.Message(
            carrier_id=settings.carrier_id,
            carrier_name=settings.carrier_name,
            code=error.get("code"),
            message=error.get("error"),
            details={**kwargs},
        )
        for error in errors
    ]


def parse_http_response(response: urllib.error.HTTPError) -> dict:
    return lib.to_json(dict(code=str(response.code), error=response.reason))
