import base64
from typing import Optional
import math

from karrio.lib import request
from karrio import lib
from karrio.core import Settings as BaseSettings


class Settings(BaseSettings):
    """Freightcom connection settings."""

    api_key: str


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

        if not self.connection_config.payment_method_type.state:
            raise Exception(f"Payment method type not set")

        cache_key = f"payment|{self.carrier_name}|{self.connection_config.payment_method_type.state}|{self.api_key}"

        payment = self.connection_cache.get(cache_key) or {}
        payment_id = payment.get("id")

        if payment_id:
            return payment_id

        self.connection_cache.set(cache_key, lambda: get_payment_id(self))
        new_auth = self.connection_cache.get(cache_key)

        return new_auth.get("id")


def download_label(file_url: str) -> str:
    return request(
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
        response = proxy._get_payments_methods()
        methods = response.deserialize()

        selected_method = next((
            method for method in methods
            if settings.connection_config.payment_method_type.type.map(
            method.get('type')).name == settings.connection_config.payment_method_type.state
        ), None)


        if not selected_method:
            raise Exception(f"Payment method {settings.connection_config.payment_method_type.stat} not found in API")

        return selected_method

    except Exception as e:
        raise
