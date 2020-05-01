"""PurplShip Freight Gateway modules."""

import attr
import pkgutil
from typing import Callable, Union
from purplship.core import Settings
from purplship.freight.proxy import Proxy
from purplship.freight.mapper import Mapper
import purplship.freight.mappers as mappers


@attr.s(auto_attribs=True)
class Gateway:
    mapper: Mapper
    proxy: Proxy
    settings: Settings


@attr.s(auto_attribs=True)
class GatewayInitializer:
    initializer: Callable[[Union[Settings, dict]], Gateway]

    def create(self, settings: dict) -> Gateway:
        return self.initializer(settings)


class _ProviderMapper:
    @property
    def providers(self):
        # Register PurplShip mappers
        return {
            name: __import__(f"{mappers.__name__}.{name}", fromlist=[name])
            for _, name, _ in pkgutil.iter_modules(mappers.__path__)
        }

    def __getitem__(self, key) -> GatewayInitializer:
        def initializer(settings: Union[Settings, dict]) -> Gateway:
            try:
                provider = self.providers[key]
                settings_value: Settings = (
                    provider.Settings(**settings)
                    if isinstance(settings, dict)
                    else settings
                )
                return Gateway(
                    settings=settings_value,
                    proxy=provider.Proxy(settings_value),
                    mapper=provider.Mapper(settings_value),
                )
            except KeyError as e:
                raise Exception(f"Unknown provider id '{key}'") from e

        return GatewayInitializer(initializer)


gateway = _ProviderMapper()
