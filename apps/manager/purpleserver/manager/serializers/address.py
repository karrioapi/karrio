from purpleserver.core.utils import owned_model_serializer
from purplship.core import utils
from purpleserver.core import gateway
from purpleserver.core.serializers import AddressData
from purpleserver.manager import models


@owned_model_serializer
class AddressSerializer(AddressData):

    def __init__(self, *args, **kwargs):
        if 'data' in kwargs and isinstance(kwargs['data'], str):
            kwargs.update(data=AddressData(models.Address.objects.get(pk=kwargs['data'])).data)

        super().__init__(*args, **kwargs)

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

    def create(self, validated_data: dict) -> models.Address:
        validated_data.update(created_by=self._context_user)
        return models.Address.objects.create(**validated_data)

    def update(self, instance: models.Address, validated_data: dict) -> models.Address:
        for key, val in validated_data.items():
            setattr(instance, key, val)

        instance.save()
        return instance
