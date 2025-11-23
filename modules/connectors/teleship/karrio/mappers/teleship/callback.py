"""Karrio Teleship client callback."""

import typing
import karrio.lib as lib
import karrio.core.models as models
import karrio.api.callback as callback
import karrio.providers.teleship as provider
import karrio.mappers.teleship.settings as provider_settings


class Callback(callback.Callback):
    settings: provider_settings.Settings

    def process_webhook_event(
        self, response: lib.Deserializable
    ) -> typing.Tuple[models.WebhookEventDetails, typing.List[models.Message]]:
        return provider.process_webhook_event(response, self.settings)

    def process_oauth_callback(
        self, response: lib.Deserializable
    ) -> typing.Tuple[typing.List[typing.Dict], typing.List[models.Message]]:
        return provider.process_oauth_callback(response, self.settings)
