"""PurplShip Freight Gateway modules."""

import attr
from typing import Callable, Union
from purplship.core import Settings
from purplship.freight.proxy import Proxy
from purplship.freight.mapper import Mapper
from purplship.freight.mappers import Providers


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
    def __getitem__(self, key) -> GatewayInitializer:
        def initializer(settings: Union[Settings, dict]) -> Gateway:
            try:
                provider = Providers[key]
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
