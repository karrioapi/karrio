import karrio.schemas.postnl.error_response as pnl
import typing
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.postnl.utils as provider_utils


def parse_error_response(
    response: typing.Union[dict, typing.List[dict]],
    settings: provider_utils.Settings,
    **kwargs,
) -> typing.List[models.Message]:
    """Parse Post NL error response."""
    responses = response if isinstance(response, list) else [response]
    error_responses = [pnl.ErrorResponseType(**res) for res in responses]
    errors: typing.List[typing.Union[pnl.ErrorType, pnl.FaultType]] = [
        [
            *([res.Error] if res.Error else []),
            *([res.fault] if res.fault else []),
            *([_ for _ in res.Errors] if res.Errors else []),
        ]
        for res in error_responses
    ]

    return [
        models.Message(
            carrier_id=settings.carrier_id,
            carrier_name=settings.carrier_name,
            code=lib.failsafe(
                lambda: e.Code or e.ErrorCode or e.Message or e.detail.errorcode
            ),
            message=(e.Description or e.ErrorDescription or e.faultstring),
            details={
                **kwargs,
                **(dict(error=e.Error) if e.Error else {}),
            },
        )
        for e in errors
    ]
