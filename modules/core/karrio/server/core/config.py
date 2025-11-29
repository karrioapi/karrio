"""Karrio server system configuration adapter."""

import typing
import karrio.lib as lib


class ConstanceConfig(lib.AbstractSystemConfig):
    """Django constance configuration adapter.

    Provides access to runtime configuration values stored
    in Django constance (database-backed settings).
    """

    def get(self, key: str, default: typing.Any = None) -> typing.Any:
        from constance import config as constance_config

        return getattr(constance_config, key, default)

    def __getitem__(self, key: str) -> typing.Any:
        from constance import config as constance_config

        return getattr(constance_config, key)

    def __contains__(self, key: str) -> bool:
        from constance import config as constance_config

        return hasattr(constance_config, key)


# Singleton instance for use across the server
config = ConstanceConfig()
