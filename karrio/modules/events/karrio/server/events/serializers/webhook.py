from karrio.server.serializers import owned_model_serializer
from karrio.server.events.serializers import WebhookData, Webhook
import karrio.server.events.models as models


@owned_model_serializer
class WebhookSerializer(WebhookData):
    def create(self, validated_data: dict, context, **kwargs) -> models.Webhook:
        return models.Webhook.objects.create(
            test_mode=getattr(context, "test_mode", False),
            **validated_data,
        )

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

        instance.save()
        return instance
