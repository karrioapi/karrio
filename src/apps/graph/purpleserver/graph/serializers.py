import typing
from django.db import transaction
from django.contrib.auth import get_user_model
from rest_framework import serializers

from purpleserver.core.utils import save_one_to_one_data, save_many_to_many_data
import purpleserver.core.validators as validators
import purpleserver.providers.models as providers
import purpleserver.manager.models as manager
import purpleserver.graph.models as graph

User = get_user_model()


class ModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = None

    def __init__(self, *args, **kwargs):
        self._extra = {}

        if 'created_by' in kwargs:
            self._extra.update(created_by=kwargs.pop('created_by'))

        super().__init__(*args, **kwargs)

    def create(self, data: dict):
        return self.Meta.model.objects.create(**data, **self._extra)

    def update(self, instance, data: dict):
        for name, value in data.items():
            setattr(instance, name, value)

        instance.save(**self._extra)
        return instance


def apply_optional_fields(serializer: typing.Type[serializers.ModelSerializer]):
    _name = f"Partial{serializer.__name__}"

    class _Meta(serializer.Meta):
        extra_kwargs = {
            field.name: {'required': False} for field in serializer.Meta.model._meta.fields
        }

    return type(_name, (serializer,), dict(Meta=_Meta))


class AddressModelSerializer(ModelSerializer, validators.AugmentedAddressSerializer):
    country_code = serializers.CharField(required=True)

    class Meta:
        model = manager.Address
        exclude = ['created_at', 'updated_at', 'created_by', 'validate_location', 'validation']


class PaymentModelSerializer(ModelSerializer):
    contact = AddressModelSerializer(required=False)

    class Meta:
        model = manager.Payment
        exclude = ['created_at', 'updated_at', 'created_by']

    @transaction.atomic
    def create(self, validated_data: dict) -> graph.Template:
        created_by = validated_data['created_by']
        data = {
            **validated_data,
            'contact': save_one_to_one_data(AddressModelSerializer, data=validated_data.get('contact'), created_by=created_by),
        }

        return super().create(data)

    @transaction.atomic
    def update(self, instance: graph.Template, validated_data: dict) -> graph.Template:
        data = {
            **validated_data,
            'contact': save_one_to_one_data(AddressModelSerializer, instance.contact, data=validated_data.get('contact')),
        }

        return super().create(data)


class CommodityModelSerializer(ModelSerializer):
    weight_unit = serializers.CharField()

    class Meta:
        model = manager.Commodity
        exclude = ['created_at', 'updated_at', 'created_by']


class CustomsModelSerializer(ModelSerializer):
    NESTED_FIELDS = ['duty', 'shipment_commodities']

    duty = apply_optional_fields(PaymentModelSerializer)(required=False)
    shipment_commodities = apply_optional_fields(CommodityModelSerializer)(many=True, required=False)

    class Meta:
        model = manager.Customs
        exclude = ['created_at', 'updated_at', 'created_by']

    @transaction.atomic
    def create(self, validated_data: dict):
        data = {
            **{name: value for name, value in validated_data.items() if name not in self.NESTED_FIELDS},
            'duty': save_one_to_one_data(PaymentModelSerializer, validated_data.get('duty'), **self._extra)
        }
        instance = super().create(data)

        save_many_to_many_data(
            CommodityModelSerializer, 'shipment_commodities', instance,
            data=validated_data.get('shipment_commodities'),
            **self._extra)

        return instance

    @transaction.atomic
    def update(self, instance: manager.Customs, validated_data: dict) -> manager.Customs:
        data = {
            **{name: value for name, value in validated_data.items() if name not in self.NESTED_FIELDS},
            'duty': save_one_to_one_data(PaymentModelSerializer, instance.duty, validated_data.get('duty'))
        }

        save_many_to_many_data(
            CommodityModelSerializer, 'shipment_commodities', instance,
            data=validated_data.get('shipment_commodities'),
            **self._extra)

        return super().update(instance, data)


class ParcelModelSerializer(validators.PresetSerializer, ModelSerializer):
    class Meta:
        model = manager.Parcel
        exclude = ['created_at', 'updated_at', 'created_by']


class UserModelSerializer(ModelSerializer):
    id = serializers.IntegerField(required=True)
    email = serializers.CharField(required=False)

    class Meta:
        model = User
        fields = ['id', 'email', 'full_name', 'is_active']


class TemplateModelSerializer(ModelSerializer):
    address = apply_optional_fields(AddressModelSerializer)(required=False)
    customs = apply_optional_fields(CustomsModelSerializer)(required=False)
    parcel = apply_optional_fields(ParcelModelSerializer)(required=False)

    class Meta:
        model = graph.Template
        exclude = ['created_at', 'updated_at', 'created_by']

    @transaction.atomic
    def create(self, validated_data: dict) -> graph.Template:
        data = {
            **validated_data,
            'address': save_one_to_one_data(AddressModelSerializer, data=validated_data.get('address'), **self._extra),
            'customs': save_one_to_one_data(CustomsModelSerializer, data=validated_data.get('customs'),  **self._extra),
            'parcel': save_one_to_one_data(ParcelModelSerializer, data=validated_data.get('parcel'), **self._extra)
        }

        ensure_unique_default_related_data(validated_data)

        return super().create(data)

    @transaction.atomic
    def update(self, instance: graph.Template, validated_data: dict) -> graph.Template:
        data = {
            **validated_data,
            'address': save_one_to_one_data(AddressModelSerializer, instance.address, data=validated_data.get('address'), partial=True),
            'customs': save_one_to_one_data(CustomsModelSerializer, instance.customs, data=validated_data.get('customs'), partial=True),
            'parcel': save_one_to_one_data(ParcelModelSerializer, instance.parcel, data=validated_data.get('parcel'), partial=True),
        }

        ensure_unique_default_related_data(validated_data, instance)

        return super().update(instance, data)


def ensure_unique_default_related_data(data: dict = None, instance: typing.Optional[graph.Template] = None):
    if (data or {}).get('is_default', getattr(instance, 'is_default', None)) is not True:
        return

    if getattr(instance, 'address', None) is not None:
        query = dict(address__isnull=False, is_default=True)
    elif getattr(instance, 'customs', None) is not None:
        query = dict(customs__isnull=False, is_default=True)
    elif getattr(instance, 'parcel', None) is not None:
        query = dict(parcel__isnull=False, is_default=True)
    else:
        return

    default_templates = graph.Template.objects.filter(**query)
    if any([template for template in default_templates if template.id != instance.id]):
        for template in default_templates:
            template.is_default = False
            template.save()


def create_carrier_model_serializers(partial: bool = False):
    def _create_model_serializer(carrier_model):
        _name = f'{carrier_model.__name__}'

        class Meta:
            model = carrier_model
            exclude = ['created_at', 'updated_at', 'created_by']

        return type(_name, (ModelSerializer,), dict(
            Meta=Meta,
            carrier_id=serializers.CharField(required=not partial)
        ))

    return {
        carrier.__name__.lower(): _create_model_serializer(carrier)
        for carrier in providers.MODELS.values()
    }


CARRIER_MODEL_SERIALIZERS = create_carrier_model_serializers()


class ConnectionModelSerializerBase(ModelSerializer):
    class Meta:
        model = providers.Carrier
        exclude = ['created_at', 'updated_at', 'created_by', 'carrier_id', 'test', 'active']

    @transaction.atomic
    def create(self, validated_data: dict):
        name, data = next(iter(validated_data.items()), ('', None))
        serializer = CARRIER_MODEL_SERIALIZERS[name]
        settings = save_one_to_one_data(serializer, data=data, **self._extra)

        return getattr(settings, 'carrier_ptr', None)

    @transaction.atomic
    def update(self, instance, validated_data: dict):
        name, data = next(iter(validated_data.items()), ('', None))
        serializer = CARRIER_MODEL_SERIALIZERS[name]
        settings = save_one_to_one_data(serializer, getattr(instance, name), data=data, partial=True)

        return getattr(settings, 'carrier_ptr', None)


ConnectionModelSerializer = type('ConnectionModelSerializer', (ConnectionModelSerializerBase,), {
    _name: _serializer(required=False)
    for _name, _serializer in CARRIER_MODEL_SERIALIZERS.items()
})

PartialConnectionModelSerializer = type('PartialConnectionModelSerializer', (ConnectionModelSerializerBase,), {
    _name: apply_optional_fields(_serializer)(required=False)
    for _name, _serializer in create_carrier_model_serializers(True).items()
})
