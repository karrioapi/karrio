from purpleserver.core.serializers import ParcelData
from purpleserver.manager.models import Parcel


class ParcelSerializer(ParcelData):

    def create(self, validated_data: dict) -> Parcel:
        return Parcel.objects.create(**validated_data)

    def update(self, instance: Parcel, validated_data: dict) -> Parcel:
        for key, val in validated_data.items():
            setattr(instance, key, val)

        instance.save()
        return instance
