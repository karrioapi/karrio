import base64
import typing
import karrio.lib as lib
import karrio.core as core


class Settings(core.Settings):
    """Sendle connection settings."""

    sendle_id: str
    api_key: str

    @property
    def carrier_name(self):
        return "sendle"

    @property
    def server_url(self):
        return (
            "https://sandbox.sendle.com" if self.test_mode else "https://api.sendle.com"
        )

    @property
    def authorization(self):
        pair = "%s:%s" % (self.sendle_id, self.api_key)
        return base64.b64encode(pair.encode("utf-8")).decode("ascii")


def check_for_order_failures(responses: typing.List[str]) -> bool:
    """Check for shipment failures."""
    _responses = [lib.to_dict(_) for _ in responses]

    return any([response.get("order_id") is None for response in _responses])


def shipment_next_call(response: dict, settings: Settings, has_failure: bool) -> dict:
    """Get next call for shipment."""
    _response = lib.to_dict(response)

    if _response.get("labels") is not None and not has_failure:
        return dict(
            method="GET",
            response=_response,
            url=_response["labels"][0]["url"],
        )

    if _response.get("order_id") is not None:
        return dict(
            method="DELETE",
            response=_response,
            url=f"{settings.server_url}/api/orders/{_response.get('order_id')}",
        )

    return dict(
        abort=True,
        response=_response,
    )


def label_decoder(response):
    _content = lib.failsafe(lambda: response.read())
    _label = lib.failsafe(lambda: lib.encode_base64(_content))
    _data = lib.failsafe(lambda: lib.to_dict(_content)) or {}

    return lib.to_dict(
        {
            **_data,
            "label": _label,
        }
    )
