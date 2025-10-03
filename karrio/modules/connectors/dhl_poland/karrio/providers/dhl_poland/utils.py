"""Karrio DHL Parcel Poland client settings."""

from karrio.schemas.dhl_poland.services import AuthData
from karrio.core.settings import Settings as BaseSettings
from karrio.core.utils import Envelope, apply_namespaceprefix, XP


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
        namespacedef_ = (
            'xmlns:soap-env="http://schemas.xmlsoap.org/soap/envelope/"'
            f' xmlns="{namesapce}"'
        )
        envelope.ns_prefix_ = "soap-env"
        envelope.Body.ns_prefix_ = envelope.ns_prefix_

        apply_namespaceprefix(envelope.Body.anytypeobjs_[0], "")
        return (
            XP.export(envelope, namespacedef_=namespacedef_)
            .replace(
                "<%s:%s" % (envelope.ns_prefix_, request_name),
                "<%s%s" % ("", request_name),
            )
            .replace(
                "</%s:%s" % (envelope.ns_prefix_, request_name),
                "</%s%s" % ("", request_name),
            )
        )
