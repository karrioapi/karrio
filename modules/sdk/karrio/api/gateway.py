"""Karrio API Gateway definition modules."""

import attr
import typing

import karrio.core as core
import karrio.api.proxy as proxy
import karrio.core.utils as utils
import karrio.api.mapper as mapper
import karrio.core.models as models
import karrio.core.errors as errors
import karrio.references as references
import karrio.api.hooks as hooks
from karrio.core.utils.logger import logger


@attr.s(auto_attribs=True)
class Gateway:
    """The carrier connection instance"""

    is_hub: bool
    proxy: proxy.Proxy
    mapper: mapper.Mapper
    tracer: utils.Tracer
    settings: core.Settings
    hooks: hooks.Hooks

    @property
    def capabilities(self) -> typing.List[str]:
        return references.detect_capabilities(self.proxy_methods, self.hooks_methods)

    @property
    def proxy_methods(self) -> typing.List[str]:
        return references.detect_proxy_methods(self.proxy.__class__)

    @property
    def hooks_methods(self) -> typing.List[str]:
        return references.detect_hooks_methods(self.hooks.__class__)

    def check(self, request: str, origin_country_code: str = None):
        messages = []

        if request not in self.proxy_methods and request not in self.hooks_methods:
            messages.append(
                models.Message(
                    carrier_id=self.settings.carrier_id,
                    carrier_name=self.settings.carrier_name,
                    code="SHIPPING_SDK_NON_SUPPORTED_ERROR",
                    message="this operation is not supported.",
                )
            )

        if (
            any(origin_country_code or "")
            and any(self.settings.account_country_code or "")
            and (origin_country_code != self.settings.account_country_code)
        ):
            messages.append(
                models.Message(
                    carrier_id=self.settings.carrier_id,
                    carrier_name=self.settings.carrier_name,
                    code="SHIPPING_SDK_ORIGIN_NOT_SERVICED_ERROR",
                    message="this account cannot ship from origin {}".format(
                        origin_country_code
                    ),
                )
            )

        return messages


@attr.s(auto_attribs=True)
class ICreate:
    """A gateway initializer type class"""

    initializer: typing.Callable[
        [
            typing.Union[core.Settings, dict],
            typing.Optional[utils.Tracer],
            typing.Optional[utils.Cache],
            typing.Optional[utils.SystemConfig],
        ],
        Gateway,
    ]

    def create(
        self,
        settings: typing.Union[core.Settings, dict],
        tracer: utils.Tracer = None,
        cache: utils.Cache = None,
        system_config: utils.SystemConfig = None,
        **kwargs,
    ) -> Gateway:
        """A gateway factory with a fluent API interface.

        Args:
            settings (Union[Settings, dict]): carrier connection configuration

        Returns:
            Gateway: The carrier connection instance
        """
        return self.initializer(settings, tracer, cache, system_config, **kwargs)


class GatewayInitializer:
    """Gateway initializer helper"""

    __instance: "GatewayInitializer" = None

    def __init__(self):
        if GatewayInitializer.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            GatewayInitializer.__instance = self

    def __getitem__(self, key: str) -> ICreate:
        """Map a provider's name to return a way to initialize it

        Args:
            key (str): a provider's name

        Returns:
            ICreate: the corresponding provider's Gateway initializer
        """

        try:
            provider = self.providers[key]

            def initializer(
                settings: typing.Union[core.Settings, dict],
                tracer: utils.Tracer = None,
                cache: utils.Cache = None,
                system_config: utils.SystemConfig = None,
                is_stub: bool = False,
            ) -> Gateway:
                """Initialize a provider gateway with the required settings

                Args:
                    settings (Union[Settings, dict]): the provider settings

                Returns:
                    Gateway: a gateway instance
                """

                try:
                    _tracer = tracer or utils.Tracer()
                    _cache = cache or utils.Cache()
                    _system_config = system_config or utils.SystemConfig()

                    if is_stub:
                        settings_value = provider.Settings.as_stub(settings)
                    else:
                        settings_value = (
                            utils.DP.to_object(provider.Settings, settings)
                            if isinstance(settings, dict)
                            else settings
                        )

                    # set cache handle to all carrier settings
                    setattr(settings_value, "cache", _cache)

                    # set tracer handle to all carrier settings
                    setattr(settings_value, "tracer", _tracer)

                    # set system config handle to all carrier settings
                    setattr(settings_value, "system_config", _system_config)

                    return Gateway(
                        tracer=_tracer,
                        is_hub=provider.is_hub,
                        settings=settings_value,
                        mapper=provider.Mapper(settings_value),
                        proxy=provider.Proxy(settings_value),
                        hooks=(
                            provider.Hooks(settings_value)
                            if provider.Hooks is not None
                            else hooks.Hooks(settings_value)
                        ),
                    )

                except Exception as er:
                    raise errors.ShippingSDKError(
                        f"Failed to setup provider '{key}'"
                    ) from er

            return ICreate(initializer)
        except KeyError as e:
            logger.error("Unknown provider requested", provider=key, error=str(e))
            raise errors.ShippingSDKError(f"Unknown provider '{key}'")

    @property
    def providers(self):
        return references.collect_providers_data()

    @staticmethod
    def get_instance() -> "GatewayInitializer":
        """Return the singleton instance of the GatewayInitializer"""

        if GatewayInitializer.__instance is None:
            GatewayInitializer()
        return GatewayInitializer.__instance


logger.info("Karrio SDK gateway initialized")
