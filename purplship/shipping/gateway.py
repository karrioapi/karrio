"""PurplShip Shipping Gateway modules."""

import attr
from enum import Enum
from typing import Callable, Union
from purplship.core import Settings
from purplship.shipping.proxy import Proxy
from purplship.shipping.mapper import Mapper

import purplship.shipping.mappers.aups
import purplship.shipping.mappers.caps
import purplship.shipping.mappers.dhl
import purplship.shipping.mappers.fedex
import purplship.shipping.mappers.ups
import purplship.shipping.mappers.usps
import purplship.shipping.mappers.sendle


class Providers(Enum):
    aups = purplship.shipping.mappers.aups
    caps = purplship.shipping.mappers.caps
    dhl = purplship.shipping.mappers.dhl
    fedex = purplship.shipping.mappers.fedex
    sendle = purplship.shipping.mappers.sendle
    ups = purplship.shipping.mappers.ups
    usps = purplship.shipping.mappers.usps


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


class ProviderMapper:
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


gateway = ProviderMapper()
