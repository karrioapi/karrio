"""Karrio DHL Freight client settings."""

import attr
import jstruct
import karrio.core.models as models
import karrio.providers.dhl_freight.units as provider_units
import karrio.providers.dhl_freight.utils as provider_utils
import karrio.universal.mappers.rating_proxy as rating_proxy


@attr.s(auto_attribs=True)
class Settings(provider_utils.Settings, rating_proxy.RatingMixinSettings):
    """DHL Freight connection settings."""

    # carrier specific properties
    client_id: str = None
    client_secret: str = None
    account_number: str = None  # consignor DHL Freight account number (Parties[Consignor].Id)
    consignee_account_number: str = None  # default consignee account (Parties[Consignee].Id)

    # generic properties
    id: str = None
    test_mode: bool = False
    carrier_id: str = "dhl_freight"
    services: list[models.ServiceLevel] = jstruct.JList[
        models.ServiceLevel, False, dict(default=provider_units.DEFAULT_SERVICES)
    ]  # type: ignore
    account_country_code: str = "DE"
    metadata: dict = {}
    config: dict = {}

    @property
    def shipping_services(self) -> list[models.ServiceLevel]:
        if any(self.services or []):
            return self.services

        return provider_units.DEFAULT_SERVICES
