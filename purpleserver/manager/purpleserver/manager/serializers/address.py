from purpleserver.core.serializers import AddressData
from purpleserver.manager.models import Address


class AddressSerializer(AddressData):

    def create(self, validated_data: dict) -> Address:
        return Address.objects.create(**validated_data)

    def update(self, instance: Address, validated_data: dict) -> Address:
        for key, val in validated_data.items():
            setattr(instance, key, val)

        instance.save()
        return instance
