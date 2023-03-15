import typing
import karrio.lib as lib
import karrio.core.models as models
import karrio.universal.providers.rating.utils as utils


def parse_rate_response(
    responses: typing.List[typing.Tuple[str, utils.PackageRates]], _
) -> typing.Tuple[typing.List[models.RateDetails], typing.List[models.Message]]:
    package_rates: typing.List[typing.Tuple[str, typing.List[models.RateDetails]]] = []
    messages: typing.List[models.Message] = []

    for _ref, _response in responses:
        _rates, _messages = _response
        messages += _messages
        package_rates += [(_ref, _rates)]

    rates = lib.to_multi_piece_rates(package_rates)

    return rates, messages


def rate_request(
    payload: models.RateRequest, _
) -> lib.Serializable[models.RateRequest]:
    return lib.Serializable(payload)
