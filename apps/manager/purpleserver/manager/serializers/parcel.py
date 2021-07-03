from purpleserver.core.serializers import ParcelData
from purpleserver.serializers import owned_model_serializer
from purpleserver.manager.models import Parcel


@owned_model_serializer
class ParcelSerializer(ParcelData):
    def create(self, validated_data: dict, **kwargs) -> Parcel:
        return Parcel.objects.create(**validated_data)

    def update(self, instance: Parcel, validated_data: dict, **kwargs) -> Parcel:
        for key, val in validated_data.items():
            setattr(instance, key, val)

        instance.save()
        return instance
