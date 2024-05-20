"""Karrio Settings abstract class definition"""

import abc
import attr
import typing


@attr.s(auto_attribs=True)
class Settings(abc.ABC):
    """Unified API carrier connection settings (Interface)"""

    carrier_id: str
    account_country_code: str = None
    test_mode: bool = False
    metadata: dict = {}
    config: dict = {}
    id: str = None

    @property
    def carrier_name(self) -> typing.Optional[str]:
        return None

    @property
    def server_url(self) -> typing.Optional[str]:
        return None

    @property
    def tracking_url(self) -> typing.Optional[str]:
        return None

    @property
    def connection_config(self):
        import karrio.lib as lib

        return lib.to_connection_config(self.config or {})

    @property
    def connection_cache(self):
        import karrio.lib as lib

        return getattr(self, "cache", None) or lib.Cache()
