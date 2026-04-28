import karrio.server.events.models as models
import karrio.server.serializers as serializers


@serializers.owned_model_serializer
class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Event
        exclude = ["created_at", "updated_at", "created_by"]
