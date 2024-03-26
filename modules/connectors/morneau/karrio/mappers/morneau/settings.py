"""Karrio Groupe Morneau client settings."""

import attr
import jstruct
import karrio.lib as lib
import karrio.providers.morneau.utils as provider_utils


@attr.s(auto_attribs=True)
class Settings(provider_utils.Settings):
    """Groupe Morneau connection settings."""

    username: str
    password: str
    billed_id: int
    caller_id: str

    division: str = "Morneau"
    carrier_id: str = "morneau"
    account_country_code: str = None
    cache: lib.Cache = jstruct.JStruct[lib.Cache, False, dict(default=lib.Cache())]
    test_mode: bool = False
    metadata: dict = {}
    id: str = None
    config: dict = {}
