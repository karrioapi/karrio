"""Karrio PostAT provider utilities."""

import attr
import karrio.lib as lib
import karrio.core as core
import karrio.core.utils as utils
from karrio.core.utils.soap import apply_namespaceprefix


def standard_request_serializer(envelope: lib.Envelope) -> str:
    """Serialize envelope to PostAT SOAP format with proper namespaces."""
    namespace_def = (
        'xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" '
        'xmlns:post="http://post.ondot.at"'
    )

    envelope.ns_prefix_ = "soapenv"
    envelope.Body.ns_prefix_ = "soapenv"

    for node in envelope.Body.anytypeobjs_:
        apply_namespaceprefix(node, "post")

    return utils.XP.export(envelope, namespacedef_=namespace_def)


@attr.s(auto_attribs=True)
class Settings(core.Settings):
    """PostAT connection settings."""

    # Required credentials (from Austrian Post onboarding)
    client_id: str
    org_unit_id: str
    org_unit_guid: str

    # Generic settings
    id: str = None
    test_mode: bool = False
    carrier_id: str = "postat"
    account_country_code: str = "AT"
    metadata: dict = {}
    config: dict = {}

    @property
    def carrier_name(self):
        return "postat"

    @property
    def server_url(self):
        """Return the server URL.

        Note: Austrian Post provides the URL during customer onboarding.
        This should be configured via connection settings.
        """
        return (
            self.connection_config.server_url.state
            or "https://plc.post.at/Post.Webservice/ShippingService.svc/secure"
        )

    @property
    def tracking_url(self):
        """Return the public tracking URL template for end users."""
        return "https://www.post.at/sv/sendungssuche?snr={}"

    @property
    def connection_config(self) -> lib.units.Options:
        """Return connection configuration options."""
        from karrio.providers.postat.units import ConnectionConfig

        return lib.to_connection_config(
            self.config or {},
            option_type=ConnectionConfig,
        )
