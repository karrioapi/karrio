from purplship.server.serializers import owned_model_serializer
from purplship.core import utils
from purplship.server.core import gateway
from purplship.server.core.serializers import AddressData
from purplship.server.manager import models


@owned_model_serializer
class AddressSerializer(AddressData):
    def validate(self, data):
        validated_data = super().validate(data)
        should_validate = (
            validated_data.get('validate_location') is True or
            (self.instance is not None and self.instance.validate_location)
        )

        if should_validate:
            address = {
                **(AddressData(self.instance).data if self.instance is not None else {}),
                **validated_data
            }
            validation = gateway.Address.validate(address)
            validated_data.update(dict(validation=utils.DP.to_dict(validation)))

        return validated_data

    def create(self, validated_data: dict, **kwargs) -> models.Address:
        return models.Address.objects.create(**validated_data)

    def update(self, instance: models.Address, validated_data: dict, **kwargs) -> models.Address:
        for key, val in validated_data.items():
            setattr(instance, key, val)

        instance.save()
        return instance
