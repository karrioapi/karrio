"""Karrio Canpar client settings."""

import karrio.lib as lib
from karrio.core.settings import Settings as BaseSettings
from karrio.core.utils import Envelope, apply_namespaceprefix, XP, Header

LanguageEnum = lib.units.create_enum("LanguageEnum", ["en", "fr"])


class Settings(BaseSettings):
    """Canpar connection settings."""

    username: str
    password: str
    language: LanguageEnum = "en"  # type: ignore

    account_country_code: str = "CA"

    @property
    def carrier_name(self):
        return "canpar"

    @property
    def server_url(self):
        return (
            "https://sandbox.canpar.com/canshipws/services"
            if self.test_mode
            else "https://canship.canpar.com/canshipws/services"
        )

    @property
    def tracking_url(self):
        return (
            "https://www.canpar.com/" + self.language + "/tracking/track.htm?barcode={}"
        )

    @staticmethod
    def serialize(
        envelope: Envelope,
        default_prefix: str = "ws",
        extra_namespace: str = "",
        special_prefixes: dict = None,
    ) -> str:

        namespacedef_ = (
            'xmlns:soap="http://www.w3.org/2003/05/soap-envelope" '
            ' xmlns:ws="http://ws.onlinerating.canshipws.canpar.com"'
            ' xmlns:xsd="http://ws.dto.canshipws.canpar.com/xsd"'
            f" {extra_namespace}"
        )
        envelope.ns_prefix_ = "soap"
        envelope.Header = Header()
        envelope.Body.ns_prefix_ = envelope.ns_prefix_
        envelope.Header.ns_prefix_ = envelope.ns_prefix_

        prefixes = {**(special_prefixes or {}), "request_children": "xsd"}

        for node in envelope.Body.anytypeobjs_ + envelope.Header.anytypeobjs_:
            apply_namespaceprefix(node, default_prefix, prefixes)

        return XP.export(envelope, namespacedef_=namespacedef_)
