import typing
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.dpd.utils as provider_utils


def parse_error_response(
    response: lib.Element,
    settings: provider_utils.Settings,
    **kwargs,
) -> typing.List[models.Message]:
    errors: typing.List[typing.Tuple[str, str]] = []
    faults: typing.List[lib.Element] = lib.find_element("Fault", response)
    details: typing.List[lib.Element] = sum(
        ([*_] for _ in lib.find_element("detail", response)), start=[]
    )

    if len(details) > 0:
        errors = [
            (_.findtext("errorCode"), _.findtext("errorMessage")) for _ in details
        ]
    elif len(faults) > 0:
        errors = [(_.findtext("faultcode"), _.findtext("faultstring")) for _ in faults]

    return [
        models.Message(
            carrier_id=settings.carrier_id,
            carrier_name=settings.carrier_name,
            code=code,
            message=message,
            details={**kwargs},
        )
        for code, message in errors
    ]
