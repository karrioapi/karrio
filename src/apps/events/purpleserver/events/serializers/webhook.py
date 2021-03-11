from purpleserver.events.serializers import WebhookData
from purpleserver.manager.models import Webhook


class WebhookSerializer(WebhookData):

    def create(self, validated_data: dict) -> Webhook:
        return Webhook.objects.create(**validated_data)

    def update(self, instance: Webhook, validated_data: dict) -> Webhook:
        for key, val in validated_data.items():
            setattr(instance, key, val)

        instance.save()
        return instance
