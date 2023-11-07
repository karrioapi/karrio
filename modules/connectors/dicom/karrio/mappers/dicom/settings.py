"""Karrio Dicom client settings."""

import attr
from karrio.providers.dicom.utils import Settings as BaseSettings


@attr.s(auto_attribs=True)
class Settings(BaseSettings):
    """Dicom connection settings."""

    # Carrier specific properties
    username: str
    password: str
    billing_account: str = None

    # Base properties
    id: str = None
    test_mode: bool = False
    carrier_id: str = "dicom"
    account_country_code: str = None
    metadata: dict = {}
    config: dict = {}
