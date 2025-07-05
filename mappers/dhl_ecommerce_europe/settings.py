"""Karrio DHL eCommerce Europe client settings."""

import attr
import karrio.providers.dhl_ecommerce_europe.utils as provider_utils


@attr.s(auto_attribs=True)
class Settings(provider_utils.Settings):
    """DHL eCommerce Europe connection settings."""

    # required carrier specific properties
    username: str
    password: str
    account_number: str = None

    # generic properties
    id: str = None
    test_mode: bool = False
    carrier_id: str = "dhl_ecommerce_europe"
    account_country_code: str = "DE"
    metadata: dict = {}
    config: dict = {}

    @property
    def test(self) -> bool:
        return self.test_mode

    @property
    def shipper_country_code(self) -> str:
        return self.account_country_code 