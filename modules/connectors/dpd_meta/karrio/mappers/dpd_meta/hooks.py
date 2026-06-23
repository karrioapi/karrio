"""Karrio DPD Meta client hooks."""

import karrio.api.hooks as hooks
import karrio.core.models as models
import karrio.mappers.dpd_meta.settings as provider_settings
import karrio.providers.dpd_meta as provider


class Hooks(hooks.Hooks):
    settings: provider_settings.Settings

    def on_webhook_event(
        self, payload: models.RequestPayload
    ) -> tuple[models.WebhookEventDetails, list[models.Message]]:
        return provider.on_webhook_event(payload, self.settings)
