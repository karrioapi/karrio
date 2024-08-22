import base64

import karrio.lib as lib
from karrio.core import Settings as BaseSettings
from karrio.core.utils import Envelope, apply_namespaceprefix, XP

LanguageEnum = lib.units.create_enum("LanguageEnum", ["en", "fr"])


class Settings(BaseSettings):
    """Purolator connection settings."""

    username: str
    password: str
    account_number: str
    user_token: str = None
    language: LanguageEnum = "en"  # type: ignore

    id: str = None
    account_country_code: str = "CA"
    metadata: dict = {}

    @property
    def carrier_name(self):
        return "purolator"

    @property
    def server_url(self):
        return (
            "https://devwebservices.purolator.com"
            if self.test_mode
            else "https://webservices.purolator.com"
        )

    @property
    def authorization(self):
        pair = "%s:%s" % (self.username, self.password)
        return base64.b64encode(pair.encode("utf-8")).decode("ascii")

    @property
    def tracking_url(self):
        return "https://tools.usps.com/go/TrackConfirmAction?tLabels={}"


def standard_request_serializer(envelope: Envelope, version: str = "v2") -> str:
    namespacedef_ = (
        'xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" '
        f'xmlns:{version}="http://purolator.com/pws/datatypes/{version}"'
    )
    envelope.ns_prefix_ = "soap"
    envelope.Body.ns_prefix_ = envelope.ns_prefix_
    envelope.Header.ns_prefix_ = envelope.ns_prefix_

    for node in envelope.Body.anytypeobjs_ + envelope.Header.anytypeobjs_:
        apply_namespaceprefix(node, version)

    return XP.export(envelope, namespacedef_=namespacedef_)
