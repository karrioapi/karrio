"""Purplship DHL Parcel Poland client settings."""

from dhl_poland_lib.services import AuthData
from purplship.core.settings import Settings as BaseSettings
from purplship.core.utils import Envelope, apply_namespaceprefix, XP


class Settings(BaseSettings):
    """DHL Parcel Poland connection settings."""

    username: str
    password: str
    account_number: str = None

    id: str = None
    account_country_code: str = "PL"

    @property
    def carrier_name(self):
        return "dhl_poland"

    @property
    def server_url(self):
        return (
            "https://sandbox.dhl24.com.pl/webapi2/provider/service.html?ws=1"
            if self.test
            else "https://dhl24.com.pl/webapi2/provider/service.html?ws=1"
        )

    @property
    def auth_data(self):
        return AuthData(
            username=self.username,
            password=self.password,
        )

    @staticmethod
    def serialize(envelope: Envelope, request_name: str) -> str:
        namespacedef_ = (
            'xmlns:soap-env="http://schemas.xmlsoap.org/soap/envelope/"'
            ' xmlns="https://sandbox.dhl24.com.pl/webapi2/provider/service.html?ws=1"'
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


DEFAULT_SERVICES = [
    {
        "service_name": "DHL Poland Premium",
        "service_code": "dhl_poland_premium",
        "cost": "0.00",
        "currency": "USD",
        "domicile": True,
    },
    {
        "service_name": "DHL Poland Polska",
        "service_code": "dhl_poland_polska",
        "cost": "0.00",
        "currency": "USD",
        "domicile": True,
    },
    {
        "service_name": "DHL Poland 09",
        "service_code": "dhl_poland_09",
        "cost": "0.00",
        "currency": "USD",
        "domicile": True,
    },
    {
        "service_name": "DHL Poland 12",
        "service_code": "dhl_poland_12",
        "cost": "0.00",
        "currency": "USD",
        "domicile": True,
    },
    {
        "service_name": "DHL Poland Connect",
        "service_code": "dhl_poland_connect",
        "cost": "0.00",
        "currency": "USD",
        "international": True,
    },
    {
        "service_name": "DHL Poland International",
        "service_code": "dhl_poland_international",
        "cost": "0.00",
        "currency": "USD",
        "international": True,
    },
]
