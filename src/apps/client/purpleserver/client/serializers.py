from typing import Dict, Any

from django.db import transaction
from rest_framework.serializers import ModelSerializer

from purpleserver.core.utils import SerializerDecorator
from purpleserver.core.serializers import Customs, Parcel, Address
import purpleserver.manager.serializers as serializers
import purpleserver.client.models as models

TemplateName = str
TEMPLATE_MODELS: Dict[str, Any] = dict(
    address=Address,
    customs=Customs,
    parcel=Parcel
)


class TemplateSerializer(ModelSerializer):
    class Meta:
        model = models.Template
        exclude = ['created_at', 'updated_at', 'user']

    address = serializers.AddressSerializer(required=False)
    customs = serializers.CustomsSerializer(required=False)
    parcel = serializers.ParcelSerializer(required=False)

    @transaction.atomic
    def create(self, validated_data: dict) -> models.Template:
        user = validated_data.get('user')
        label = validated_data.get('label')
        related_data = {}

        if 'address' in validated_data:
            related_data = dict(
                address=SerializerDecorator[serializers.AddressSerializer](
                    data=validated_data.get('address')).save(user=user).instance)

        elif 'customs' in validated_data:
            related_data = dict(
                customs=SerializerDecorator[serializers.CustomsSerializer](
                    data=validated_data.get('customs')).save(user=user).instance)

        elif 'parcel' in validated_data:
            related_data = dict(
                parcel=SerializerDecorator[serializers.ParcelSerializer](
                    data=validated_data.get('parcel')).save(user=user).instance)

        template = models.Template.objects.create(**{
            'user': user,
            'label': label,
            **related_data,
        })
        return template

    @transaction.atomic
    def update(self, instance: models.Template, validated_data: dict) -> models.Template:
        instance.label = validated_data.get('label', instance.label)

        if 'address' in validated_data:
            data = validated_data.get('address')
            if instance.address is not None and data is None:
                instance.address.delete()
                instance.address = None
            else:
                instance.address = SerializerDecorator[serializers.AddressSerializer](
                    instance.address, data=data).save().instance

        if 'customs' in validated_data:
            data = validated_data.get('customs')
            if instance.customs is not None and data is None:
                instance.customs.delete()
                instance.customs = None
            else:
                instance.customs = SerializerDecorator[serializers.CustomsSerializer](
                    instance.customs, data=data).save().instance

        if 'parcel' in validated_data:
            data = validated_data.get('parcel')
            if instance.parcel is not None and data is None:
                instance.parcel.delete()
                instance.parcel = None
            else:
                instance.parcel = SerializerDecorator[serializers.ParcelSerializer](
                    instance.parcel, data=data).save().instance

        instance.save()
        return instance
