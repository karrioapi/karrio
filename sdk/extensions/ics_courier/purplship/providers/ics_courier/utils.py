"""purplship ICS Courier client settings."""

from purplship.core.settings import Settings as BaseSettings
from purplship.core.utils import Envelope, apply_namespaceprefix, XP, Header


class Settings(BaseSettings):
    """ICS Courier connection settings."""

    account_id: str
    password: str

    id: str = None
    account_country_code: str = "CA"

    @property
    def carrier_name(self):
        return "ics_courier"

    @property
    def server_url(self):
        return (
            "http://www1.icscourier.ca/icsapiwebservice/service.asmx"
            if self.test
            else "http://www1.icscourier.ca/icsapicnswebservice/service.asmx"
        )

    @staticmethod
    def serialize(envelope: Envelope, special_prefixes: dict = {}) -> str:
        namespacedef_ = (
            'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" '
            'xmlns: xsd="http://www.w3.org/2001/XMLSchema" '
            'xmlns: soap12="http://www.w3.org/2003/05/soap-envelope"'
        )
        envelope.ns_prefix_ = "soap12"
        envelope.Header = Header()
        envelope.Body.ns_prefix_ = envelope.ns_prefix_
        envelope.Header.ns_prefix_ = envelope.ns_prefix_

        prefixes = special_prefixes

        for node in envelope.Body.anytypeobjs_ + envelope.Header.anytypeobjs_:
            apply_namespaceprefix(node, "", prefixes)

        return XP.export(envelope, namespacedef_=namespacedef_)
