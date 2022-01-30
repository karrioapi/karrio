import purplship.server.serializers as serializers
import purplship.server.events.models as models


@serializers.owned_model_serializer
class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Event
        exclude = ["created_at", "updated_at", "created_by"]
