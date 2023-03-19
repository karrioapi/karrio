"""Karrio DPD client settings."""

import attr
import typing
import jstruct
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.dpd.utils as provider_utils
import karrio.providers.dpd.units as provider_units


@attr.s(auto_attribs=True)
class Settings(provider_utils.Settings):
    """DPD connection settings."""

    # required carrier specific properties
    delis_id: str
    password: str
    depot: str = None
    message_language: str = "en_EN"

    # generic properties
    id: str = None
    test_mode: bool = False
    carrier_id: str = "dpd"
    account_country_code: str = "BE"
    services: typing.List[models.ServiceLevel] = jstruct.JList[models.ServiceLevel, False, dict(default=provider_units.DEFAULT_SERVICES)]  # type: ignore
    metadata: dict = {}
    cache: lib.Cache = jstruct.JStruct[lib.Cache]
