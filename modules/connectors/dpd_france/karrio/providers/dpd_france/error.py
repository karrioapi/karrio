"""DPD France error parser.

cargoNET returns access errors (e.g., IpPermissionDenied) as a top-level
<Error><ErrorId/><ErrorMessage/></Error> document. Per-operation error
patterns will be added once observed in live responses.
"""

import typing
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.dpd_france.utils as provider_utils


def parse_error_response(
    response: lib.Element,
    settings: provider_utils.Settings,
    **kwargs,
) -> typing.List[models.Message]:
    nested = lib.find_element("Error", response)
    errors = nested if nested else ([response] if getattr(response, "tag", None) == "Error" else [])
    return [
        models.Message(
            carrier_id=settings.carrier_id,
            carrier_name=settings.carrier_name,
            code=error.findtext("ErrorId") or "",
            message=error.findtext("ErrorMessage") or "",
            details={**kwargs},
        )
        for error in errors
    ]
