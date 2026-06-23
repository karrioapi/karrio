import karrio.core.models as models
import karrio.lib as lib
import karrio.providers.bpost.utils as provider_utils
import karrio.schemas.bpost.business_exception as business
import karrio.schemas.bpost.system_exception as system


def parse_error_response(
    response: lib.Element,
    settings: provider_utils.Settings,
    **kwargs,
) -> list[models.Message]:
    errors = [
        *lib.find_element("systemException", response, system.systemException),
        *lib.find_element("businessException", response, business.businessException),
    ]

    if "systemException" in getattr(response, "tag", None):
        errors.append(lib.to_object(system.systemException, response))

    if "businessException" in getattr(response, "tag", None):
        errors.append(lib.to_object(business.businessException, response))

    return [
        models.Message(
            carrier_id=settings.carrier_id,
            carrier_name=settings.carrier_name,
            code=getattr(error, "code", "500"),
            message=getattr(error, "message", "").strip(),
            details={**kwargs},
        )
        for error in errors
    ]
