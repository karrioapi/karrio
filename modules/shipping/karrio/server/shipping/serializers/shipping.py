import karrio.server.serializers as serializers
import karrio.server.shipping.models as models


@serializers.owned_model_serializer
class ShippingMethodModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ShippingMethod
        exclude = ["created_at", "updated_at", "created_by"]
        extra_kwargs = {field: {"read_only": True} for field in ["id"]}
