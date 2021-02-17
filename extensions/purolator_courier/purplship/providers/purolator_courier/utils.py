from base64 import b64encode
from purplship.core import Settings as BaseSettings
from purplship.core.utils import Envelope, apply_namespaceprefix, XP


class Settings(BaseSettings):
    """UPS connection settings."""

    username: str
    password: str
    account_number: str
    user_token: str
    language: str = "en"
    id: str = None

    @property
    def carrier_name(self):
        return "purolator_courier"

    @property
    def server_url(self):
        return (
            "https://devwebservices.purolator.com"
            if self.test
            else "https://webservices.purolator.com"
        )

    @property
    def authorization(self):
        pair = "%s:%s" % (self.username, self.password)
        return b64encode(pair.encode("utf-8")).decode("ascii")


def standard_request_serializer(envelope: Envelope, version: str = "v2") -> str:
    namespacedef_ = f'xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" xmlns:{version}="http://purolator.com/pws/datatypes/{version}"'
    envelope.ns_prefix_ = "soap"
    envelope.Body.ns_prefix_ = envelope.ns_prefix_
    envelope.Header.ns_prefix_ = envelope.ns_prefix_
    [
        apply_namespaceprefix(node, version)
        for node in (envelope.Body.anytypeobjs_ + envelope.Header.anytypeobjs_)
    ]
    return XP.export(envelope, namespacedef_=namespacedef_)
