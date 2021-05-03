from purpleserver.core.serializers import CommodityData, Commodity
from purpleserver.core.utils import owned_model_serializer
import purpleserver.manager.models as models


@owned_model_serializer
class CommoditySerializer(Commodity):

    def __init__(self, *args, **kwargs):
        if 'data' in kwargs and isinstance(kwargs['data'], str):
            kwargs.update(data=CommodityData(models.Commodity.objects.get(pk=kwargs['data'])).data)

        super().__init__(*args, **kwargs)

    def create(self, validated_data: dict) -> Commodity:
        validated_data.update(created_by=self._context_user)
        return models.Commodity.objects.create(**validated_data)

    def update(self, instance: models.Commodity, validated_data: dict) -> models.Commodity:
        for key, val in validated_data.items():
            setattr(instance, key, val)

        instance.save()
        return instance
