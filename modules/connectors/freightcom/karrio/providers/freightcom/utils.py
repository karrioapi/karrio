import base64
from typing import Optional
import math

from karrio import lib
from karrio.core import Settings as BaseSettings
from karrio.providers.freightcom.units import PaymentMethodType


class Settings(BaseSettings):
    """Freightcom connection settings."""

    api_key: str
    payment_method_type: PaymentMethodType = PaymentMethodType.net_terms


    account_country_code: str = None
    metadata: dict = {}
    config: dict = {}

    @property
    def server_url(self):
        return (
            "https://customer-external-api.ssd-test.freightcom.com"
            if self.test_mode
            else "https://external-api.freightcom.com"
        )

    @property
    def carrier_name(self):
        return "freightcom"

    @property
    def connection_config(self) -> lib.units.Options:
        from karrio.providers.freightcom.units import ConnectionConfig

        return lib.to_connection_config(
            self.config or {},
            option_type=ConnectionConfig,
        )

    @property
    def payment_method(self):
        cache_key = f"payment|{self.carrier_name}|{self.payment_method_type}|{self.api_key}"

        payment = self.connection_cache.get(cache_key) or {}
        payment_id = payment.get("id")

        if payment_id:
            return payment_id

        self.connection_cache.set(cache_key, lambda: get_payment_id(self))
        new_auth = self.connection_cache.get(cache_key)

        return new_auth.get("id")


def download_label(file_url: str) -> str:
    return lib.request(
        decoder=lambda b: base64.encodebytes(b).decode("utf-8"),
        url=file_url,
    )


def ceil(value: Optional[float]) -> Optional[int]:
    if value is None:
        return None
    return math.ceil(value)

def get_payment_id(settings: Settings) -> dict:

    try:
        from karrio.mappers.freightcom.proxy import Proxy

        proxy = Proxy(settings)
        response = proxy.get_payments_methods()
        methods = response.deserialize()


    except Exception as e:
        raise


    for method in methods:
        if PaymentMethodType.map(method.get('type')).name == settings.payment_method_type:
            return method

    else:
        raise Exception(f"Payment method {settings.payment_method_type} not found")
