import karrio.server.serializers as serializers
import karrio.server.documents.models as models


@serializers.owned_model_serializer
class DocumentTemplateModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.DocumentTemplate
        exclude = ["created_at", "updated_at", "created_by"]
