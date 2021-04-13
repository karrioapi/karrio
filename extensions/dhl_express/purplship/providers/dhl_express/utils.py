import time
from dhl_express_lib.datatypes_global_v62 import ServiceHeader, Request
from purplship.core import Settings as BaseSettings


class Settings(BaseSettings):
    """DHL connection settings."""

    site_id: str
    password: str
    account_number: str = None
    id: str = None

    @property
    def carrier_name(self):
        return "dhl_express"

    @property
    def server_url(self):
        return (
            "https://xmlpitest-ea.dhl.com/XMLShippingServlet"
            if self.test else
            "https://xmlpi-ea.dhl.com/XMLShippingServlet"
        )

    def Request(self, **kwargs) -> Request:
        return Request(
            ServiceHeader=ServiceHeader(
                MessageReference="1234567890123456789012345678901",
                MessageTime=time.strftime("%Y-%m-%dT%H:%M:%S"),
                SiteID=self.site_id,
                Password=self.password,
            ),
            **kwargs,
        )


def reformat_time(tag: str, xml_str: str) -> str:
    """
    Change time format from 00:00:00 to 00:00
    """
    parts = xml_str.split(tag)
    subs = parts[1].split(":")
    return f"{parts[0]}{tag}{subs[0]}:{subs[1]}</{tag}{parts[2]}"
