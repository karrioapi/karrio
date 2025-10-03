import karrio.server.serializers as serializers
import karrio.server.shipping.models as models


@serializers.owned_model_serializer
class ShippingMethodModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ShippingMethod
