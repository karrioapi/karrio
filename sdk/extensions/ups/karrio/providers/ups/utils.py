import ups_lib.ups_security as ups
import typing
import karrio.lib as lib
import karrio.core.units as units
from karrio.core import Settings as BaseSettings


class Settings(BaseSettings):
    """UPS connection settings."""

    username: str
    password: str
    access_license_number: str
    account_number: str = None
    account_country_code: str = None
    metadata: dict = {}
    config: dict = {}

    id: str = None

    @property
    def carrier_name(self):
        return "ups"

    @property
    def server_url(self):
        return (
            "https://wwwcie.ups.com"
            if self.test_mode
            else "https://onlinetools.ups.com"
        )

    @property
    def Security(self):
        return ups.UPSSecurity(
            UsernameToken=ups.UsernameTokenType(
                Username=self.username, Password=self.password
            ),
            ServiceAccessToken=ups.ServiceAccessTokenType(
                AccessLicenseNumber=self.access_license_number
            ),
        )

    @property
    def default_currency(self) -> typing.Optional[str]:
        if self.account_country_code in SUPPORTED_COUNTRY_CURRENCY:
            return units.CountryCurrency.map(self.account_country_code).value

        return "USD"

    @property
    def tracking_url(self):
        return "https://www.ups.com/track?loc=en_US&requester=QUIC&tracknum={}/trackdetails"

    @property
    def connection_config(self) -> lib.units.Options:
        from karrio.providers.ups.units import ConnectionConfig

        return lib.to_connection_config(
            self.config or {},
            option_type=ConnectionConfig,
        )


def default_request_serializer(
    prefix: str,
    namespace: str,
) -> typing.Callable[[lib.Envelope], str]:
    def serializer(envelope: lib.Envelope):
        namespace_ = (
            'xmlns:tns="http://schemas.xmlsoap.org/soap/envelope/"'
            ' xmlns:xsd="http://www.w3.org/2001/XMLSchema"'
            ' xmlns:upss="http://www.ups.com/XMLSchema/XOLTWS/UPSS/v1.0"'
            ' xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"'
            ' xmlns:common="http://www.ups.com/XMLSchema/XOLTWS/Common/v1.0"'
            f" {namespace}"
        )
        envelope.Body.ns_prefix_ = envelope.ns_prefix_
        envelope.Header.ns_prefix_ = envelope.ns_prefix_
        lib.apply_namespaceprefix(envelope.Body.anytypeobjs_[0], prefix)
        lib.apply_namespaceprefix(envelope.Header.anytypeobjs_[0], "upss")
        lib.apply_namespaceprefix(envelope.Body.anytypeobjs_[0].Request, "common")

        return lib.to_xml(envelope, namespacedef_=namespace_)

    return serializer


SUPPORTED_COUNTRY_CURRENCY = ["US", "CA", "FR", "FR", "AU"]
