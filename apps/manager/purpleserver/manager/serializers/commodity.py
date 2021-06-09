from purpleserver.core.serializers import CommodityData, Commodity
from purpleserver.serializers import owned_model_serializer
import purpleserver.manager.models as models


@owned_model_serializer
class CommoditySerializer(Commodity):
    def create(self, validated_data: dict, **kwargs) -> Commodity:
        return models.Commodity.objects.create(**validated_data)

    def update(self, instance: models.Commodity, validated_data: dict, **kwargs) -> models.Commodity:
        for key, val in validated_data.items():
            setattr(instance, key, val)

        instance.save()
        return instance
