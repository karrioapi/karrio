import karrio.server.serializers as serializers
import karrio.server.tenants.models as models


class TenantModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Client
        exclude = ["created_at", "updated_at"]


class DomainModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Domain
        exclude: list = []
