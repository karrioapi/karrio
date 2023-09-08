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
        error for error in results if error.get("error_code") is not None
    ]

    return [
        models.Message(
            carrier_id=settings.carrier_id,
            carrier_name=settings.carrier_name,
            code=error.get("error_code"),
            message=error.get("error_message"),
            details={**kwargs},
        )
        for error in errors
    ]


def parse_http_error(error: urllib.error.HTTPError) -> dict:
    return dict(
        error_code=str(error.code),
        error_message=error.reason,
    )
