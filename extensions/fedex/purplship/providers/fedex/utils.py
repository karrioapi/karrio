from typing import Callable
from purplship.core import Settings as BaseSettings
from purplship.core.utils import Envelope, apply_namespaceprefix, XP
from fedex_lib.rate_service_v26 import (
    WebAuthenticationCredential,
    WebAuthenticationDetail,
    ClientDetail,
)


class Settings(BaseSettings):
    """FedEx connection settings."""

    user_key: str
    password: str
    meter_number: str
    account_number: str
    id: str = None

    @property
    def server_url(self):
        return (
            "https://wsbeta.fedex.com:443/web-services"
            if self.test
            else "https://ws.fedex.com:443/web-services"
        )

    @property
    def webAuthenticationDetail(self) -> WebAuthenticationDetail:
        return WebAuthenticationDetail(
            UserCredential=WebAuthenticationCredential(
                Key=self.user_key, Password=self.password
            )
        )

    @property
    def clientDetail(self) -> ClientDetail:
        return ClientDetail(
            AccountNumber=self.account_number, MeterNumber=self.meter_number
        )


def default_request_serializer(
    prefix: str, namespace: str
) -> Callable[[Envelope], str]:
    def serializer(envelope: Envelope):
        namespacedef_ = f'xmlns:tns="http://schemas.xmlsoap.org/soap/envelope/" {namespace}'

        envelope.Body.ns_prefix_ = envelope.ns_prefix_
        apply_namespaceprefix(envelope.Body.anytypeobjs_[0], prefix)

        return XP.export(envelope, namespacedef_=namespacedef_)

    return serializer
