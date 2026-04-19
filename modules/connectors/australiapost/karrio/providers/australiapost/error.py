import karrio.core.models as models
import karrio.lib as lib
import karrio.providers.australiapost.utils as provider_utils
import karrio.schemas.australiapost.error_response as australiapost


def parse_error_response(
    response: dict,
    settings: provider_utils.Settings,
    **kwargs,
) -> list[models.Message]:
    responses = response if isinstance(response, list) else [response]
    error_list: list[dict] = sum(
        [
            *[res.get("errors", []) for res in responses if "errors" in res],
            *[res.get("warnings", []) for res in responses if "warnings" in res],
        ],
        [],
    )
    errors: list[australiapost.ErrorType] = [lib.to_object(australiapost.ErrorType, error) for error in error_list]

    return [
        models.Message(
            carrier_id=settings.carrier_id,
            carrier_name=settings.carrier_name,
            code=(error.code or error.error_code or error.error),
            message=(error.message or error.error_description or error.name),
            details=lib.to_dict(
                {
                    **kwargs,
                    "field": error.field,
                    "context": error.context,
                    "messages": error.messages,
                }
            ),
        )
        for error in errors
    ]
