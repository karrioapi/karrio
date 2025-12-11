
import base64
import datetime
import karrio.lib as lib
import karrio.core as core
import karrio.core.errors as errors
from karrio.core.utils.caching import ThreadSafeTokenManager


class Settings(core.Settings):
    """DPD Group connection settings."""

    # DPD META-API authentication properties
    # Required
    bucode: str  # Business Unit code (X-DPD-BUCODE)

    # Authentication method 1: Username/Password
    username: str = None  # X-DPD-LOGIN
    password: str = None  # X-DPD-PASSWORD

    # Authentication method 2: Client credentials
    client_id: str = None  # X-DPD-CLIENTID
    client_secret: str = None  # X-DPD-CLIENTSECRET

    # Optional account information
    account_number: str = None
    customer_account_number: str = None

    @property
    def carrier_name(self):
        return "dpd_group"

    @property
    def server_url(self):
        return (
            "https://api-preprod.dpsin.dpdgroup.com:8443/shipping/v1"
            if self.test_mode
            else "https://api.dpdgroup.com/shipping/v1"
        )

    @property
    def tracking_url(self):
        return "https://www.dpdgroup.com/tracking?parcelNumber={}"

    @property
    def connection_config(self) -> lib.units.Options:
        from karrio.providers.dpd_group.units import ConnectionConfig

        return lib.to_connection_config(
            self.config or {},
            option_type=ConnectionConfig,
        )
