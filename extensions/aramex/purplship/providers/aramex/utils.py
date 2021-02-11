from purplship.core.utils import XP, apply_namespaceprefix, Envelope, Header
from purplship.core import Settings as BaseSettings


class Settings(BaseSettings):
    """Aramex connection settings."""

    # Carrier specific properties
    username: str
    password: str
    account_pin: str
    account_entity: str
    account_number: str
    account_country_code: str

    id: str = None

    @property
    def carrier_name(self):
        return "aramex"

    @property
    def server_url(self):
        return (
            "http://ws.dev.aramex.net"
            if self.test
            else "http://ws.aramex.net"
        )

    @staticmethod
    def standard_request_serializer(
            envelope: Envelope, version: str = "v1", extra_namespace: str = "", special_prefixes: dict = None) -> str:

        namespacedef_ = (
            f'xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" '
            f'xmlns:{version}="http://ws.aramex.net/ShippingAPI/{version}/" '
            f'{extra_namespace}'
        )
        envelope.ns_prefix_ = "soap"
        envelope.Header = Header()
        envelope.Body.ns_prefix_ = envelope.ns_prefix_
        envelope.Header.ns_prefix_ = envelope.ns_prefix_

        for node in (envelope.Body.anytypeobjs_ + envelope.Header.anytypeobjs_):
            apply_namespaceprefix(node, version, special_prefixes)

        return XP.export(envelope, namespacedef_=namespacedef_)
