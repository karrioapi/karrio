from purplship.server.core.serializers import ParcelData
from purplship.server.serializers import owned_model_serializer, save_many_to_many_data

from purplship.server.manager.serializers.commodity import CommoditySerializer
import purplship.server.manager.models as models


@owned_model_serializer
class ParcelSerializer(ParcelData):
    def __init__(self, instance: models.Address = None, **kwargs):
        data = kwargs.get("data") or {}

        if ("items" in data) and (instance is not None):
            save_many_to_many_data(
                "items",
                CommoditySerializer,
                instance,
                payload=data,
                context=getattr(self, "__context", None),
            )

        super().__init__(instance, **kwargs)

    def create(self, validated_data: dict, context: dict, **kwargs) -> models.Parcel:
        instance = models.Parcel.objects.create(
            **{key: value for key, value in validated_data.items() if key != "items"}
        )

        save_many_to_many_data(
            "items",
            CommoditySerializer,
            instance,
            payload=validated_data,
            context=context,
        )

        return instance

    def update(
        self, instance: models.Parcel, validated_data: dict, **kwargs
    ) -> models.Parcel:
        for key, val in validated_data.items():
            setattr(instance, key, val)

        instance.save()
        return instance
