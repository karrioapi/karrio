import karrio.schemas.roadie.error as roadie
import typing
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.roadie.utils as provider_utils


def parse_error_response(
    response: dict,
    settings: provider_utils.Settings,
    **kwargs,
) -> typing.List[models.Message]:
    responses: typing.List[dict] = sum(
        [
            res.get("errors", [])
            for res in (response if isinstance(response, list) else [response])
        ],
        start=[],
    )
    errors = [lib.to_object(roadie.ErrorElement, res) for res in responses]

    return [
        models.Message(
            carrier_id=settings.carrier_id,
            carrier_name=settings.carrier_name,
            code=error.code,
            message=error.message,
            details={
                **kwargs,
                **(dict(parameters=error.parameter) if error.parameter else {}),
            },
        )
        for error in errors
    ]
