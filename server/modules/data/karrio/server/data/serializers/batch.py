import karrio.server.serializers as serializers
import karrio.server.data.models as models


@serializers.owned_model_serializer
class BatchOperationModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.BatchOperation
        exclude = ["created_at", "updated_at", "created_by"]
