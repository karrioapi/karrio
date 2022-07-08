from typing import Callable
from karrio.core import Settings as BaseSettings
from karrio.core.utils import Envelope, apply_namespaceprefix, XP
from ups_lib.ups_security import UPSSecurity, UsernameTokenType, ServiceAccessTokenType


class Settings(BaseSettings):
    """UPS connection settings."""

    username: str
    password: str
    access_license_number: str
    account_number: str = None
    account_country_code: str = None
    metadata: dict = {}

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
        return UPSSecurity(
            UsernameToken=UsernameTokenType(
                Username=self.username, Password=self.password
            ),
            ServiceAccessToken=ServiceAccessTokenType(
                AccessLicenseNumber=self.access_license_number
            ),
        )


def default_request_serializer(
    prefix: str, namespace: str
) -> Callable[[Envelope], str]:
    def serializer(envelope: Envelope):
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
        apply_namespaceprefix(envelope.Body.anytypeobjs_[0], prefix)
        apply_namespaceprefix(envelope.Header.anytypeobjs_[0], "upss")
        apply_namespaceprefix(envelope.Body.anytypeobjs_[0].Request, "common")

        return XP.export(envelope, namespacedef_=namespace_)

    return serializer
