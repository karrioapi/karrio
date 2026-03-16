import karrio.schemas.dhl_express.datatypes_global_v62 as dhl
import time
import typing
import karrio.lib as lib
import karrio.core as core
import karrio.core.units as units


class Settings(core.Settings):
    """DHL connection settings."""

    site_id: str
    password: str
    account_number: str = None
    account_country_code: str = None
    metadata: dict = {}

    id: str = None

    @property
    def carrier_name(self):
        return "dhl_express"

    @property
    def server_url(self):
        return (
            "https://xmlpitest-ea.dhl.com"
            if self.test_mode
            else "https://xmlpi-ea.dhl.com"
        )

    @property
    def tracking_url(self):
        return "https://www.dhl.com/ca-en/home/tracking/tracking-parcel.html?submit=1&tracking-id={}"

    @property
    def connection_config(self) -> lib.units.Options:
        from karrio.providers.dhl_express.units import ConnectionConfig

        return lib.to_connection_config(
            self.config or {},
            option_type=ConnectionConfig,
        )

    @property
    def default_currency(self) -> typing.Optional[str]:
        return units.CountryCurrency.map(self.account_country_code).value or "USD"

    def Request(self, **kwargs) -> dhl.Request:
        return dhl.Request(
            ServiceHeader=dhl.ServiceHeader(
                MessageReference="1234567890123456789012345678901",
                MessageTime=time.strftime("%Y-%m-%dT%H:%M:%S"),
                SiteID=self.site_id,
                Password=self.password,
            ),
            **kwargs,
        )


def reformat_time(tag: str, xml_str: str) -> str:
    """Change time format from 00:00:00 to 00:00"""
    parts = xml_str.split(tag)
    subs = parts[1].split(":")
    return f"{parts[0]}{tag}{subs[0]}:{subs[1]}</{tag}{parts[2]}"
