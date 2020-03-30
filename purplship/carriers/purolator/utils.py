from purplship.core import Settings as BaseSettings
from purplship.core.utils.soap import Envelope
from purplship.core.utils.helpers import export


class Settings(BaseSettings):
    """UPS connection settings."""

    user_token: str
    account_number: str
    language: str = 'en'
    id: str = None

    @property
    def carrier(self):
        return 'purolator'


def standard_request_serializer(envelope: Envelope) -> str:
    namespacedef_ = 'xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/" xmlns:ns1="http://purolator.com/pws/datatypes/v1"'
    envelope.ns_prefix_ = "SOAP-ENV"
    envelope.Body.ns_prefix_ = envelope.ns_prefix_
    envelope.Header.ns_prefix_ = envelope.ns_prefix_
    envelope.Body.anytypeobjs_[0].ns_prefix_ = "ns1"
    envelope.Header.anytypeobjs_[0].ns_prefix_ = "ns1"
    return export(envelope, namespacedef_=namespacedef_)
