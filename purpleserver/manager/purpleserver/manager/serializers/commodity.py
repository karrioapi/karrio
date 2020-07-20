from purpleserver.core.serializers import CommodityData
from purpleserver.manager.models import Commodity


class CommoditySerializer(CommodityData):

    def create(self, validated_data: dict) -> Commodity:
        return Commodity.objects.create(**validated_data)

    def update(self, instance: Commodity, validated_data: dict) -> Commodity:
        for key, val in validated_data.items():
            setattr(instance, key, val)

        instance.save()
        return instance
