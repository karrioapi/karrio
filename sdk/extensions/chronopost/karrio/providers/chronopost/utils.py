"""Karrio Chronopost client settings."""

from chronopost_lib.shippingservice import headerValue
from karrio.core.settings import Settings as BaseSettings
from karrio.core.utils import Envelope, apply_namespaceprefix, XP


class Settings(BaseSettings):
    """Chronopost connection settings."""

    account_number: str
    password: str
    id_emit: str = "CHRFR"

    account_country_code: str = "FR"

    @property
    def carrier_name(self):
        return "chronopost"

    @property
    def server_url(self):
        return "https://ws.chronopost.fr"

    @property
    def header_value(self):
        return headerValue(accountNumber=self.account_number, idEmit=self.id_emit)

    @staticmethod
    def serialize(envelope: Envelope, request_name: str, namesapce: str) -> str:
        namespacedef_ = (
            'xmlns:soap-env="http://schemas.xmlsoap.org/soap/envelope/"'
            f' xmlns="{namesapce}"'
        )
        envelope.ns_prefix_ = "soapenv"
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
