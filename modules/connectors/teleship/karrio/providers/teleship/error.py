import typing
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.teleship.utils as provider_utils
import karrio.schemas.teleship.error_response as teleship


def parse_error_response(
    response: typing.Union[dict, list],
    settings: provider_utils.Settings,
    **kwargs,
) -> typing.List[models.Message]:
    """Parse Teleship error response"""

    errors = lib.failsafe(lambda: response.get("messages")) or []

    # Handle single error format
    if isinstance(response, dict) and response.get("error"):
        error_obj = response.get("error")
        if isinstance(error_obj, dict):
            errors = [error_obj]
        elif isinstance(error_obj, list):
            errors = error_obj

    # Handle messages array format
    if isinstance(errors, list) and any(errors):
        return [
            models.Message(
                carrier_id=settings.carrier_id,
                carrier_name=settings.carrier_name,
                code=str(error.get("code", "")),
                message=error.get("message", ""),
                level=error.get("level"),
                details=lib.to_dict(
                    {
                        **kwargs,
                        "timestamp": error.get("timestamp"),
                        "details": error.get("details"),
                    }
                ),
            )
            for error in errors
        ]

    return []
