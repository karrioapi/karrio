from purplship.server.serializers import owned_model_serializer, ModelSerializer
from purplship.server.events.models import Event


@owned_model_serializer
class EventSerializer(ModelSerializer):
    class Meta:
        model = Event
        exclude = ["created_at", "updated_at", "created_by"]
