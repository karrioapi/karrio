import karrio.server.shipping.models as models
import karrio.server.shipping.serializers as serializers


@serializers.owned_model_serializer
class ShippingMethodModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ShippingMethod
