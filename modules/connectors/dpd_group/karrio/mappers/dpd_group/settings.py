"""Karrio DPD Group client settings."""

import attr
import karrio.providers.dpd_group.utils as provider_utils


@attr.s(auto_attribs=True)
class Settings(provider_utils.Settings):
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

    # generic properties (DO NOT MODIFY)
    id: str = None
    test_mode: bool = False
    carrier_id: str = "dpd_group"
    account_country_code: str = None
    metadata: dict = {}
    config: dict = {}
