"""Karrio DPD client settings."""

import attr
import typing
import jstruct.types as jstruct
import karrio.core.models as models
import karrio.providers.dpd.utils as provider_utils


@attr.s(auto_attribs=True)
class Settings(provider_utils.Settings):
    """DPD connection settings."""

    # required carrier specific properties
    delis_id: str
    password: str
    message_language: str = "en_EN"

    # generic properties
    id: str = None
    test_mode: bool = False
    carrier_id: str = "dpd"
    account_country_code: str = "BE"
    metadata: dict = {}
    services: typing.List[models.ServiceLevel] = jstruct.JList[models.ServiceLevel]  # type: ignore
