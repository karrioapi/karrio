import dpdhl_lib.business_interface as dpdhl
import typing
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.dpdhl.utils as provider_utils


def parse_error_response(
    response: lib.Element,
    settings: provider_utils.Settings,
    **kwargs,
) -> typing.List[models.Message]:
    errors: typing.List[dpdhl.Statusinformation] = [
        status
        for status in lib.find_element("Status", response, dpdhl.Statusinformation)
        if (status.statusText != "ok")
    ]

    return [
        models.Message(
            carrier_id=settings.carrier_id,
            carrier_name=settings.carrier_name,
            code=error.statusCode,
            message=error.statusText,
            details={
                **(
                    {"message": lib.join(*error.statusMessage, join=" ")}
                    if any(error.statusMessage)
                    else {}
                ),
                **(
                    {"error": error.errorMessage}
                    if any(error.errorMessage or "")
                    else {}
                ),
                **(
                    {"warning": error.warningMessage}
                    if any(error.warningMessage or "")
                    else {}
                ),
                **kwargs,
            },
        )
        for error in errors
        if any(error.statusMessage)
    ]
