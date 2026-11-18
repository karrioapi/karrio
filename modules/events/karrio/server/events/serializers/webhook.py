from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework.exceptions import ValidationError
from karrio.server.events.webhook_http import resolve_destination
from karrio.server.serializers import owned_model_serializer
from karrio.server.events.serializers import WebhookData, Webhook  # noqa: F401 - view exports
import karrio.server.events.models as models


@owned_model_serializer
class WebhookSerializer(WebhookData):
    def validate_url(self, value):
        try:
            if self.instance is None or self.instance.url != value:
                resolve_destination(value)
        except DjangoValidationError as error:
            raise ValidationError(error.messages) from error
        return value

    def create(self, validated_data: dict, context, **kwargs) -> models.Webhook:
        try:
            return models.Webhook.objects.create(
                test_mode=getattr(context, "test_mode", False),
                **validated_data,
            )
        except DjangoValidationError as error:
            raise ValidationError({"url": error.messages}) from error

    def update(
        self, instance: models.Webhook, validated_data: dict, **kwargs
    ) -> models.Webhook:
        if (
            "disabled" in validated_data
            and validated_data["disabled"] != instance.disabled
        ):
            instance.failure_streak_count = 0

        for key, val in validated_data.items():
            setattr(instance, key, val)

        try:
            instance.save()
        except DjangoValidationError as error:
            raise ValidationError({"url": error.messages}) from error
        return instance
