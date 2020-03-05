"""PurplShip Shipping Gateway modules."""

import attr
from enum import Enum
from typing import Callable, Union
from purplship.core import Settings
from purplship.package.proxy import Proxy
from purplship.package.mapper import Mapper

import purplship.package.mappers.aups
import purplship.package.mappers.caps
import purplship.package.mappers.dhl
import purplship.package.mappers.fedex
import purplship.package.mappers.ups
import purplship.package.mappers.usps
import purplship.package.mappers.sendle


class Providers(Enum):
    aups = purplship.package.mappers.aups
    caps = purplship.package.mappers.caps
    dhl = purplship.package.mappers.dhl
    fedex = purplship.package.mappers.fedex
    sendle = purplship.package.mappers.sendle
    ups = purplship.package.mappers.ups
    usps = purplship.package.mappers.usps


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
                settings: provider.Settings = provider.Settings(**settings) if isinstance(settings, dict) else settings
                return Gateway(
                    settings=settings,
                    proxy=provider.Proxy(settings),
                    mapper=provider.Mapper(settings)
                )
            except KeyError as e:
                raise Exception(f"Unknown provider id '{key}'") from e

        return GatewayInitializer(initializer)


gateway = _ProviderMapper()
