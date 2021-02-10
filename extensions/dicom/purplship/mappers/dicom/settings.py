"""Purplship Dicom client settings."""

import attr
from purplship.providers.dicom.utils import Settings as BaseSettings


@attr.s(auto_attribs=True)
class Settings(BaseSettings):
    """Dicom connection settings."""

    # Carrier specific properties
    username: str
    password: str
    billing_account: str = None

    # Base properties
    id: str = None
    test: bool = False
    carrier_id: str = "dicom"
