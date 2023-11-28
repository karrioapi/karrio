import typing
import urllib.error
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.zoom2u.utils as provider_utils


def parse_error_response(
    responses: typing.Union[typing.List[dict], dict],
    settings: provider_utils.Settings,
    **kwargs,
) -> typing.List[models.Message]:
    results = responses if isinstance(responses, list) else [responses]
    errors: typing.List[dict] = [
        error for error in results if error.get("message") is not None
    ]

    return [
        models.Message(
            carrier_id=settings.carrier_id,
            carrier_name=settings.carrier_name,
            code=error.get("error-code"),
            message=error.get("message"),
            details=lib.to_dict(
                {
                    **kwargs,
                    "modelState": error.get("modelState"),
                }
            ),
        )
        for error in errors
    ]


def parse_http_response(response: urllib.error.HTTPError) -> dict:
    try:
        return lib.decode(response.read())
    except Exception:
        pass

    return lib.to_json(
        {
            "error-code": response.code,
            "message": response.reason,
        }
    )
