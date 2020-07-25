from purpleserver.core.serializers import CommodityData
from purpleserver.manager.models import Commodity


class CommoditySerializer(CommodityData):

    def __init__(self, *args, **kwargs):
        if 'data' in kwargs and isinstance(kwargs['data'], str):
            kwargs.update(
                data=CommodityData(Commodity.objects.get(pk=kwargs['data'])).data
            )

        super().__init__(*args, **kwargs)

    def create(self, validated_data: dict) -> Commodity:
        return Commodity.objects.create(**validated_data)

    def update(self, instance: Commodity, validated_data: dict) -> Commodity:
        for key, val in validated_data.items():
            setattr(instance, key, val)

        instance.save()
        return instance
