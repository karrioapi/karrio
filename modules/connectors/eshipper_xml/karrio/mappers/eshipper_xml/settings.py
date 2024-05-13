<<<<<<< HEAD:modules/connectors/eshipper/karrio/mappers/eshipper/settings.py
"""Karrio eShipper client settings."""

import attr
import karrio.providers.eshipper.utils as provider_utils


@attr.s(auto_attribs=True)
class Settings(provider_utils.Settings):
    """eShipper connection settings."""
=======
"""Karrio eshipper_xml connection settings."""

import attr
from karrio.providers.eshipper_xml.utils import Settings as BaseSettings


@attr.s(auto_attribs=True)
class Settings(BaseSettings):
    """eshipper_xml connection settings."""
>>>>>>> 3ccfd84c0 (feat: Rename legacy eshipper integration eshipper_xml):modules/connectors/eshipper_xml/karrio/mappers/eshipper_xml/settings.py

    # required carrier specific properties
    principal: str
    credential: str

    # generic properties
    id: str = None
    test_mode: bool = False
    carrier_id: str = "eshipper_xml"
    account_country_code: str = None
    metadata: dict = {}
    config: dict = {}
