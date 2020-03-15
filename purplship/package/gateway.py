"""PurplShip Shipping Gateway modules."""

import attr
from enum import Enum
from typing import Callable, Union
from purplship.core import Settings
from purplship.package.proxy import Proxy
from purplship.package.mapper import Mapper
from purplship.package.mappers import *


class Providers(Enum):
    aups = aups
    caps = caps
    dhl = dhl
    fedex = fedex
    purolator = purolator
    sendle = sendle
    ups = ups
    usps = usps


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
                provider = Providers[key].value
                settings_value = (
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
