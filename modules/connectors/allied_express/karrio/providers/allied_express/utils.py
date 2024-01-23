import attr
import base64
import typing
import karrio.lib as lib
import karrio.core as core


class Settings(core.Settings):
    """Allied Express connection settings."""

    username: str
    password: str
    account: str = None
    service_type: str = "R"

    account_country_code: str = "AU"

    @property
    def carrier_name(self):
        return "allied_express"

    @property
    def server_url(self):
        return self.connection_config.server_url.state or (
            "https://test.aet.mskaleem.com" if self.test_mode else "https://3plapi.com"
        )

    @property
    def authorization(self):
        pair = "%s:%s" % (self.username, self.password)
        return base64.b64encode(pair.encode("utf-8")).decode("ascii")

    @property
    def connection_config(self) -> lib.units.Options:
        from karrio.providers.allied_express.units import ConnectionConfig

        return lib.to_connection_config(
            self.config or {},
            option_type=ConnectionConfig,
        )


@attr.s(auto_attribs=True)
class AlliedResponse:
    error: typing.Union[str, None] = None
    body: typing.Union[dict, None] = None
    data: typing.Union[dict, None] = None
    envelope: typing.Union[dict, None] = None
    response: typing.Union[dict, None] = None
    is_error: typing.Union[bool, None] = None


def parse_response(response: str) -> AlliedResponse:
    _response = lib.failsafe(
        lambda: lib.to_dict(
            (
                response.replace("soapenv:", "soapenv")
                .replace("@xmlns:", "xmlns")
                .replace("ns1:", "ns1")
            )
        )
    )

    if _response is None:
        _error = response[: response.find(": {")].strip()
        return AlliedResponse(
            error=_error if any(_error) else response,
            is_error=True,
        )

    _envelope = _response.get("soapenvEnvelope") or {}
    _body = _envelope.get("soapenvBody") or _response.get("soapenvBody") or {}

    if "ns1getShipmentsStatusResponse" in _body:
        _data = _body["ns1getShipmentsStatusResponse"]
        return AlliedResponse(
            data=_data,
            body=_body,
            envelope=_envelope,
            response=_response,
            is_error=(
                ("statusError" in (_data or {}).get("result", {}))
                or ("errors" in (_data or {}).get("result", {}))
            ),
        )

    if "ns1calculatePriceResponse" in _body:
        _data = _body["ns1calculatePriceResponse"]
        return AlliedResponse(
            data=_data,
            body=_body,
            envelope=_envelope,
            response=_response,
            is_error=(
                ("statusError" in (_data or {}).get("result", {}))
                or ("errors" in (_data or {}).get("result", {}))
            ),
        )

    if "ns1cancelDispatchJobResponse" in _body:
        _data = _body["ns1cancelDispatchJobResponse"]
        return AlliedResponse(
            data=_data,
            body=_body,
            envelope=_envelope,
            response=_response,
            is_error=(
                ((_data or {}).get("result") != "0")
                or ("statusError" in (_data or {}).get("result", {}))
                or ("errors" in (_data or {}).get("result", {}))
            ),
        )

    if "ns1getLabelResponse" in _body:
        _data = _body["ns1getLabelResponse"]
        return AlliedResponse(
            data=_data,
            body=_body,
            envelope=_envelope,
            response=_response,
            is_error=(
                ("statusError" in (_data or {}).get("result", {}))
                or ("errors" in (_data or {}).get("result", {}))
            ),
        )

    return AlliedResponse(
        body=_body,
        data=_response,
        envelope=_envelope,
        response=_response,
    )
