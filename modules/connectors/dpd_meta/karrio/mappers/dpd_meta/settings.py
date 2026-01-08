"""Karrio DPD Group client settings."""

import attr
import typing
import jstruct
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.dpd_meta.units as provider_units
import karrio.providers.dpd_meta.utils as provider_utils
import karrio.universal.mappers.rating_proxy as rating_proxy


@attr.s(auto_attribs=True)
class Settings(provider_utils.Settings, rating_proxy.RatingMixinSettings):
    """DPD Group connection settings."""

    # Authentication method 1: Login credentials
    dpd_login: str = None  # X-DPD-LOGIN
    dpd_password: str = None  # X-DPD-PASSWORD

    # Authentication method 2: Client credentials (for SEUR)
    dpd_client_id: str = None  # X-DPD-CLIENTID
    dpd_client_secret: str = None  # X-DPD-CLIENTSECRET

    # Customer information
    customer_id: str = None  # DPD customer ID (customerInfos.customerID)
    customer_account_number: str = None  # DPD account number
    customer_sub_account_number: str = None  # DPD sub-account number

    # generic properties (DO NOT MODIFY)
    id: str = None
    test_mode: bool = False
    carrier_id: str = "dpd_meta"
    services: typing.List[models.ServiceLevel] = jstruct.JList[models.ServiceLevel, False, dict(default=provider_units.DEFAULT_SERVICES)]  # type: ignore
    account_country_code: str = None
    metadata: dict = {}
    config: dict = {}

    @property
    def dpd_bucode(self):
        return lib.identity(
            self.connection_config.bucode.state
            or provider_units.BusinessUnit.map(self.account_country_code).value
        )

    @property
    def shipping_services(self) -> typing.List[models.ServiceLevel]:
        if any(self.services or []):
            return self.services

        return provider_units.DEFAULT_SERVICES
