import base64
import typing
import jstruct
import datetime
import karrio.lib as lib
import karrio.core as core


class Settings(core.Settings):
    """TGE connection settings."""

    username: str
    password: str
    api_key: str
    toll_username: str
    toll_password: str
    my_toll_token: str
    my_toll_identity: str
    account_code: str = None
    sscc_count: int = None
    shipment_count: int = None

    @property
    def carrier_name(self):
        return "tge"

    @property
    def server_url(self):
        return self.connection_config.server_url.state or "https://tge.3plapi.com"

    @property
    def auth(self):
        pair = "%s:%s" % (self.toll_username, self.toll_password)
        return base64.b64encode(pair.encode("utf-8")).decode("ascii")

    @property
    def authorization(self):
        pair = "%s:%s" % (self.username, self.password)
        return base64.b64encode(pair.encode("utf-8")).decode("ascii")

    @property
    def connection_config(self) -> lib.units.Options:
        from karrio.providers.tge.units import ConnectionConfig

        return lib.to_connection_config(
            self.config or {},
            option_type=ConnectionConfig,
        )

    def next_shipment_identifiers(
        self, options: lib.units.Options, package_count: int
    ) -> typing.Tuple[str, list, int, int]:
        # get state from cache
        cache_key = f"{self.carrier_name}|{self.api_key}"
        state = self.connection_cache.get(cache_key) or {}

        sscc_gs1 = lib.to_int(lib.text(self.connection_config.SSCC_GS1.state) or "")
        ship_gs1 = lib.to_int(lib.text(self.connection_config.SHIP_GS1.state) or "")
        sscc_count = (
            self.sscc_count
            if self.sscc_count is not None
            else lib.to_int(self.connection_config.SSCC_range_start.state) or 0
        )
        shipment_count = (
            self.shipment_count
            if self.shipment_count is not None
            else lib.to_int(self.connection_config.SHIP_range_start.state) or 0
        )

        if "tge_ssc_ids" in options:
            SSCCs = options.tge_ssc_ids.state
        else:
            SSCCs = [
                f"00{calculate_sscc(sscc_gs1, sscc_count, _)}"
                for _, __ in enumerate(range(package_count), start=1)
            ]

        if "tge_shipment_ids" in options:
            ShipmentIDs = options.tge_shipment_ids.state
        else:
            ShipmentIDs = [
                f"{ship_gs1}{str(shipment_count + _).zfill(7)}"
                for _, __ in enumerate(range(package_count), start=1)
            ]

        # save in cache
        _sscc_count = sscc_count + package_count
        _shipment_count = shipment_count + package_count

        self.connection_cache.set(
            cache_key,
            {**state, "sscc_count": _sscc_count, "shipment_count": _shipment_count},
        )

        return (
            ShipmentIDs,
            SSCCs,
            _shipment_count,
            _sscc_count,
        )


def parse_response(response: str) -> dict:
    _response = lib.failsafe(lambda: lib.to_dict(response))

    if _response is None:
        _error = response[: response.find(": {")].strip()
        return dict(
            message=_error if any(_error) else response,
            is_error=True,
        )

    return _response


def next_pickup_date(
    date_str: typing.Union[datetime.datetime, str]
) -> datetime.datetime:
    date = lib.to_date(date_str)

    # return next business day
    if date.weekday() == 5:
        return date + datetime.timedelta(days=3)

    return date + datetime.timedelta(days=1)


def calculate_sscc(gs1, sscc: int, index: int) -> str:
    _new_sscc = sscc + index
    _current = [int(_) for _ in f"{gs1}{_new_sscc}".zfill(17)]
    _odd_sum = sum([int(x) for _, x in enumerate(_current) if _ % 2 == 0])
    _even_sum = sum([int(x) for _, x in enumerate(_current) if _ % 2 != 0])
    _sscc_sum = (_odd_sum * 3) + _even_sum
    _nearest_multiple_of_ten = _sscc_sum + 10 - (_sscc_sum % 10)
    _digit = _nearest_multiple_of_ten - _sscc_sum

    return f"{''.join([str(_) for _ in _current])}{_digit}".zfill(18)
