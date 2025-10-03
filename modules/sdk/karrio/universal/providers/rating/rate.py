import typing
import karrio.lib as lib
import karrio.core.models as models
import karrio.universal.providers.rating.utils as utils

ResponseType = typing.List[typing.Tuple[str, utils.PackageRates]]


def parse_rate_response(
    _response: lib.Deserializable[ResponseType], _
) -> typing.Tuple[typing.List[models.RateDetails], typing.List[models.Message]]:
    responses = _response.deserialize()
    package_rates: typing.List[typing.Tuple[str, typing.List[models.RateDetails]]] = []
    messages: typing.List[models.Message] = []

    for _ref, _res in responses:
        _rates, _messages = _res
        messages += _messages
        package_rates += [(_ref, _rates)]

    rates = lib.to_multi_piece_rates(package_rates)

    return rates, messages


def rate_request(payload: models.RateRequest, _) -> lib.Serializable:
    return lib.Serializable(payload)
