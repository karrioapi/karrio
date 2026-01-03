"""ParcelOne connection utilities and settings."""

import karrio.lib as lib
import karrio.core as core


class Settings(core.Settings):
    """ParcelOne connection settings."""

    # Required credentials
    username: str
    password: str
    mandator_id: str
    consigner_id: str

    # Optional settings
    cep_id: str = None  # Default carrier (DHL, DPD, UPS, GLS, HERMES)
    product_id: str = None  # Default product code

    # Generic properties
    id: str = None
    test_mode: bool = False
    carrier_id: str = "parcelone"
    account_country_code: str = "DE"
    metadata: dict = {}
    config: dict = {}

    @property
    def carrier_name(self):
        return "parcelone"

    @property
    def server_url(self):
        return (
            "https://sandboxapi.awiwe.solutions/version4/shippingwcfsandbox/ShippingWCF.svc"
            if self.test_mode
            else "https://productionapi.awiwe.solutions/version4/shippingwcf/ShippingWCF.svc"
        )

    @property
    def tracking_url(self):
        return "https://tracking.parcel.one/?trackingNumber={}"

    @property
    def connection_config(self) -> lib.units.Options:
        from karrio.providers.parcelone.units import ConnectionConfig

        return lib.to_connection_config(
            self.config or {},
            option_type=ConnectionConfig,
        )


# XML Namespace definitions
NAMESPACES = {
    "soapenv": "http://schemas.xmlsoap.org/soap/envelope/",
    "tns": "http://tempuri.org/",
    "wcf": "http://schemas.datacontract.org/2004/07/ShippingWCF",
    "arr": "http://schemas.microsoft.com/2003/10/Serialization/Arrays",
    "wsse": "http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd",
}


def create_envelope(body: str, settings: Settings) -> str:
    """Build SOAP envelope with WS-Security header."""
    return f"""<?xml version="1.0" encoding="utf-8"?>
<soapenv:Envelope
    xmlns:soapenv="{NAMESPACES['soapenv']}"
    xmlns:tns="{NAMESPACES['tns']}"
    xmlns:wcf="{NAMESPACES['wcf']}"
    xmlns:arr="{NAMESPACES['arr']}">
    <soapenv:Header>
        <wsse:Security xmlns:wsse="{NAMESPACES['wsse']}">
            <wsse:UsernameToken>
                <wsse:Username>{settings.username}</wsse:Username>
                <wsse:Password Type="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-username-token-profile-1.0#PasswordText">{settings.password}</wsse:Password>
            </wsse:UsernameToken>
        </wsse:Security>
    </soapenv:Header>
    <soapenv:Body>
        {body}
    </soapenv:Body>
</soapenv:Envelope>"""


def xml_escape(value: str) -> str:
    """Escape special XML characters."""
    if value is None:
        return ""
    return (
        str(value)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
        .replace("'", "&apos;")
    )


def build_element(tag: str, value, namespace: str = "wcf") -> str:
    """Build a single XML element if value is not None."""
    if value is None:
        return ""
    prefix = f"{namespace}:" if namespace else ""
    return f"<{prefix}{tag}>{xml_escape(value)}</{prefix}{tag}>"


def build_optional_element(tag: str, value, namespace: str = "wcf") -> str:
    """Build an optional XML element (returns empty string if value is None)."""
    return build_element(tag, value, namespace) if value is not None else ""
