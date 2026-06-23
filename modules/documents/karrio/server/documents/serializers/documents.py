import karrio.server.documents.models as models
import karrio.server.serializers as serializers


@serializers.owned_model_serializer
class DocumentTemplateModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.DocumentTemplate
        exclude = ["created_at", "updated_at", "created_by"]
