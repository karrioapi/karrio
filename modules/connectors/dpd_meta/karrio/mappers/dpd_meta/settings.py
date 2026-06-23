"""Karrio DPD Meta client settings."""

import attr
import jstruct
import karrio.core.models as models
import karrio.providers.dpd_meta.units as provider_units
import karrio.providers.dpd_meta.utils as provider_utils
import karrio.universal.mappers.rating_proxy as rating_proxy


@attr.s(auto_attribs=True)
class Settings(provider_utils.Settings, rating_proxy.RatingMixinSettings):
    """DPD Meta connection settings.

    The META-API accepts one of two credential pairs, always alongside the
    business-unit code (`dpd_bucode`):
      • `dpd_login` + `dpd_password`          — delisId / password (most accounts)
      • `dpd_client_id` + `dpd_client_secret` — client credentials (e.g. SEUR)

    `dpd_login` is the DPD **delisId**; together with `dpd_password` it also
    authenticates the public SOAP web services (LoginService / DepotDataService)
    that resolve the sending depot.
    """

    # Credentials — provide either the login pair or the client pair.
    dpd_login: str = None  # delisId — X-DPD-LOGIN header + DepotDataService login
    dpd_password: str = None  # X-DPD-PASSWORD header + DepotDataService password
    dpd_client_id: str = None  # X-DPD-CLIENTID header (client-credential accounts)
    dpd_client_secret: str = None  # X-DPD-CLIENTSECRET header (client-credential accounts)

    # Business unit — selects the DPD org (001=DE, 002=FR, 010=NL, 011=GB, ...).
    dpd_bucode: str = None  # X-DPD-BUCODE header

    # Customer identifiers (used for billing / printed on the label).
    customer_id: str = None  # DPD customer ID — customerInfos.customerID
    customer_account_number: str = None  # DPD account number
    customer_sub_account_number: str = None  # DPD sub-account number

    # generic properties (DO NOT MODIFY)
    id: str = None
    test_mode: bool = False
    carrier_id: str = "dpd_meta"
    services: list[models.ServiceLevel] = jstruct.JList[
        models.ServiceLevel, False, dict(default=provider_units.DEFAULT_SERVICES)
    ]  # type: ignore
    account_country_code: str = None
    metadata: dict = {}
    config: dict = {}

    @property
    def shipping_services(self) -> list[models.ServiceLevel]:
        if any(self.services or []):
            return self.services

        return provider_units.DEFAULT_SERVICES
