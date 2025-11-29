"""Karrio Teleship client hooks."""

import typing
import karrio.lib as lib
import karrio.core.models as models
import karrio.api.hooks as hooks
import karrio.providers.teleship as provider
import karrio.mappers.teleship.settings as provider_settings


class Hooks(hooks.Hooks):
    settings: provider_settings.Settings

    def on_webhook_event(
        self, payload: models.RequestPayload
    ) -> typing.Tuple[models.WebhookEventDetails, typing.List[models.Message]]:
        return provider.on_webhook_event(payload, self.settings)

    def on_oauth_authorize(
        self, payload: models.OAuthAuthorizePayload
    ) -> typing.Tuple[models.OAuthAuthorizeRequest, typing.List[models.Message]]:
        return provider.on_oauth_authorize(payload, self.settings)

    def on_oauth_callback(
        self, payload: models.RequestPayload
    ) -> typing.Tuple[typing.List[typing.Dict], typing.List[models.Message]]:
        return provider.on_oauth_callback(payload, self.settings)
