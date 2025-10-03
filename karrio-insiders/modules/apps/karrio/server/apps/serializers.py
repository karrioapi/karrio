import karrio.server.serializers as serializers
import karrio.server.apps.models as models


@serializers.owned_model_serializer
class OAuthAppModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.OAuthApp
        exclude = ["created_at", "updated_at", "created_by"]


@serializers.owned_model_serializer
class AppInstallationModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AppInstallation
        exclude = ["created_at", "updated_at", "created_by"]
