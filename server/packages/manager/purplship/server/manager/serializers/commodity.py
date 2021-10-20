from purplship.server.core.serializers import CommodityData, Commodity
from purplship.server.serializers import owned_model_serializer
import purplship.server.manager.models as models


@owned_model_serializer
class CommoditySerializer(Commodity):
    def create(self, validated_data: dict, **kwargs) -> Commodity:
        return models.Commodity.objects.create(**validated_data)

    def update(self, instance: models.Commodity, validated_data: dict, **kwargs) -> models.Commodity:
        for key, val in validated_data.items():
            setattr(instance, key, val)

        instance.save()
        return instance
