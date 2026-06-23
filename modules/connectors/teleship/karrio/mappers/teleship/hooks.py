"""Karrio Teleship client hooks."""

import karrio.api.hooks as hooks
import karrio.core.models as models
import karrio.mappers.teleship.settings as provider_settings
import karrio.providers.teleship as provider


class Hooks(hooks.Hooks):
    settings: provider_settings.Settings

    def on_webhook_event(
        self, payload: models.RequestPayload
    ) -> tuple[models.WebhookEventDetails, list[models.Message]]:
        return provider.on_webhook_event(payload, self.settings)

    def on_oauth_authorize(
        self, payload: models.OAuthAuthorizePayload
    ) -> tuple[models.OAuthAuthorizeRequest, list[models.Message]]:
        return provider.on_oauth_authorize(payload, self.settings)

    def on_oauth_callback(self, payload: models.RequestPayload) -> tuple[list[dict], list[models.Message]]:
        return provider.on_oauth_callback(payload, self.settings)
