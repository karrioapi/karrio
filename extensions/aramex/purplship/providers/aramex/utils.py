from purplship.core.utils import XP, apply_namespaceprefix, Envelope
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
            "http://ws.dev.aramex.net/shippingapi"
            if self.test
            else "http://ws.aramex.net/shippingapi"
        )

    @staticmethod
    def standard_request_serializer(envelope: Envelope, version: str = "v1") -> str:
        namespacedef_ = f'xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" xmlns:{version}="http://ws.aramex.net/ShippingAPI/{version}/"'
        envelope.ns_prefix_ = "soap"
        envelope.Body.ns_prefix_ = envelope.ns_prefix_
        [
            apply_namespaceprefix(node, version)
            for node in (envelope.Body.anytypeobjs_ + envelope.Header.anytypeobjs_)
        ]
        return XP.export(envelope, namespacedef_=namespacedef_)
