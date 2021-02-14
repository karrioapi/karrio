"""Purplship Canpar client settings."""

from purplship.core.settings import Settings as BaseSettings
from purplship.core.utils import Envelope, apply_namespaceprefix, XP, Header


class Settings(BaseSettings):
    """Canpar connection settings."""

    username: str
    password: str
    language: str = "en"
    id: str = None

    @property
    def carrier_name(self):
        return "canpar"

    @property
    def server_url(self):
        return (
            'https://sandbox.canpar.com/canshipws/services'
            if self.test else
            'https://canship.canpar.com/canshipws/services'
        )

    @staticmethod
    def serialize(envelope: Envelope, default_prefix: str = "ws", extra_namespace: str = "", special_prefixes: dict = None) -> str:

        namespacedef_ = (
            'xmlns:soap="http://www.w3.org/2003/05/soap-envelope" '
            ' xmlns:ws="http://ws.onlinerating.canshipws.canpar.com"'
            ' xmlns:xsd="http://ws.dto.canshipws.canpar.com/xsd"'
            f' {extra_namespace}'
        )
        envelope.ns_prefix_ = "soap"
        envelope.Header = Header()
        envelope.Body.ns_prefix_ = envelope.ns_prefix_
        envelope.Header.ns_prefix_ = envelope.ns_prefix_

        prefixes = {**(special_prefixes or {}), 'request_children': 'xsd'}

        for node in (envelope.Body.anytypeobjs_ + envelope.Header.anytypeobjs_):
            apply_namespaceprefix(node, default_prefix, prefixes)

        return XP.export(envelope, namespacedef_=namespacedef_)
