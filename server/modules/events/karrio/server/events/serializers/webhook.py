from karrio.server.serializers import owned_model_serializer
from karrio.server.events.serializers import WebhookData
from karrio.server.events.models import Webhook


@owned_model_serializer
class WebhookSerializer(WebhookData):
    def create(self, validated_data: dict, context, **kwargs) -> Webhook:
        return Webhook.objects.create(
            test_mode=getattr(context, "test_mode", False),
            **validated_data,
        )

    def update(self, instance: Webhook, validated_data: dict, **kwargs) -> Webhook:
        for key, val in validated_data.items():
            setattr(instance, key, val)

        instance.save()
        return instance
