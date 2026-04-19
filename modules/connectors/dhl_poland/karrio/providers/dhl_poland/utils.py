"""Karrio DHL Parcel Poland client settings."""

from karrio.core.settings import Settings as BaseSettings
from karrio.core.utils import XP, Envelope, apply_namespaceprefix
from karrio.schemas.dhl_poland.services import AuthData


class Settings(BaseSettings):
    """DHL Parcel Poland connection settings."""

    username: str
    password: str
    account_number: str = None

    id: str = None
    account_country_code: str = "PL"
    metadata: dict = {}

    @property
    def carrier_name(self):
        return "dhl_poland"

    @property
    def server_url(self):
        return (
            "https://sandbox.dhl24.com.pl/webapi2/provider/service.html?ws=1"
            if self.test_mode
            else "https://dhl24.com.pl/webapi2/provider/service.html?ws=1"
        )

    @property
    def tracking_url(self):
        return "https://www.dhl.com/pl-en/home/tracking/tracking-parcel.html?submit=1&tracking-id={}"

    @property
    def auth_data(self):
        return AuthData(
            username=self.username,
            password=self.password,
        )

    @staticmethod
    def serialize(envelope: Envelope, request_name: str, namesapce: str) -> str:
        namespacedef_ = f'xmlns:soap-env="http://schemas.xmlsoap.org/soap/envelope/" xmlns="{namesapce}"'
        envelope.ns_prefix_ = "soap-env"
        envelope.Body.ns_prefix_ = envelope.ns_prefix_

        apply_namespaceprefix(envelope.Body.anytypeobjs_[0], "")
        return (
            XP.export(envelope, namespacedef_=namespacedef_)
            .replace(
                f"<{envelope.ns_prefix_}:{request_name}",
                f"<{request_name}",
            )
            .replace(
                f"</{envelope.ns_prefix_}:{request_name}",
                f"</{request_name}",
            )
        )
