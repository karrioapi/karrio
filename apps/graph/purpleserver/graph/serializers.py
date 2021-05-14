import typing
from django.db import transaction
from django.contrib.auth import get_user_model
from rest_framework.serializers import ModelSerializer as BaseModelSerializer

from purplship.core.utils import DP
from purpleserver.core.utils import save_one_to_one_data, save_many_to_many_data
import purpleserver.core.serializers as serializers
import purpleserver.core.validators as validators
import purpleserver.providers.models as providers
import purpleserver.manager.models as manager
import purpleserver.graph.models as graph

User = get_user_model()


class ModelSerializer(BaseModelSerializer):
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
            if name != 'created_by':
                setattr(instance, name, value)

        instance.save()
        return instance


def apply_optional_fields(serializer: typing.Type[BaseModelSerializer]):
    _name = f"Partial{serializer.__name__}"

    class _Meta(serializer.Meta):
        extra_kwargs = {
            **getattr(serializer.Meta, 'extra_kwargs', {}),
            **{field.name: {'required': False} for field in serializer.Meta.model._meta.fields}
        }

    return type(_name, (serializer,), dict(Meta=_Meta))


class AddressModelSerializer(validators.AugmentedAddressSerializer, ModelSerializer):
    country_code = serializers.CharField(required=False)

    class Meta:
        model = manager.Address
        extra_kwargs = {
            **{key: {'required': True} for key in ['country_code']},
            **{key: {'read_only': False} for key in ['validate_location', 'validation']},
        }
        exclude = ['created_at', 'updated_at', 'created_by']


class CommodityModelSerializer(ModelSerializer):
    weight_unit = serializers.CharField()

    class Meta:
        model = manager.Commodity
        exclude = ['created_at', 'updated_at', 'created_by']


class CustomsModelSerializer(ModelSerializer):
    NESTED_FIELDS = ['commodities']

    commodities = apply_optional_fields(CommodityModelSerializer)(many=True, allow_null=True, required=False)

    class Meta:
        model = manager.Customs
        exclude = ['created_at', 'updated_at', 'created_by', 'options']

    @transaction.atomic
    def create(self, validated_data: dict):
        data = {
            **{name: value for name, value in validated_data.items() if name not in self.NESTED_FIELDS},
            'options': DP.to_dict(validated_data['options']) if 'options' in validated_data else None,
            'duty': DP.to_dict(validated_data['duty']) if 'duty' in validated_data else None
        }

        instance = super().create(data)

        save_many_to_many_data(
            'commodities', CommodityModelSerializer, instance, payload=validated_data, **self._extra)

        return instance

    @transaction.atomic
    def update(self, instance: manager.Customs, validated_data: dict) -> manager.Customs:
        data = {
            **{name: value for name, value in validated_data.items() if name not in self.NESTED_FIELDS},
            'options': DP.to_dict(validated_data['options']) if 'options' in validated_data else instance.options,
            'duty': DP.to_dict(validated_data['duty']) if 'duty' in validated_data else instance.duty
        }

        return super().update(instance, data)


class ParcelModelSerializer(validators.PresetSerializer, ModelSerializer):
    class Meta:
        model = manager.Parcel
        exclude = ['created_at', 'updated_at', 'created_by']


class UserModelSerializer(ModelSerializer):
    email = serializers.CharField(required=False)

    class Meta:
        model = User
        extra_kwargs = {
            field: {'read_only': True} for field in ['is_staff', 'last_login', 'date_joined']
        }
        fields = ['email', 'full_name', 'is_active', 'is_staff', 'last_login', 'date_joined']


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
            'address': save_one_to_one_data('address', AddressModelSerializer, payload=validated_data, **self._extra),
            'customs': save_one_to_one_data('customs', CustomsModelSerializer, payload=validated_data, **self._extra),
            'parcel': save_one_to_one_data('parcel', ParcelModelSerializer, payload=validated_data, **self._extra)
        }

        ensure_unique_default_related_data(validated_data)

        return super().create(data)

    @transaction.atomic
    def update(self, instance: graph.Template, validated_data: dict) -> graph.Template:
        data = {key: value for key, value in validated_data.items() if key not in ['address', 'customs', 'parcel']}

        save_one_to_one_data(
            'address', AddressModelSerializer, instance, payload=validated_data, partial=True, **self._extra)
        save_one_to_one_data(
            'customs', CustomsModelSerializer, instance, payload=validated_data, partial=True, **self._extra)
        save_one_to_one_data(
            'parcel', ParcelModelSerializer, instance, payload=validated_data, partial=True, **self._extra)

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


class DefaultTemplateSerializer(serializers.EntitySerializer):
    label = serializers.CharField()
    is_default = serializers.BooleanField()
    address = serializers.AddressData(required=False)
    customs = serializers.CustomsData(required=False)
    parcel = serializers.ParcelData(required=False)


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
        name = next(iter(validated_data.keys()), '')
        serializer = CARRIER_MODEL_SERIALIZERS[name]
        settings = save_one_to_one_data(name, serializer, payload=validated_data, **self._extra)

        return getattr(settings, 'carrier_ptr', None)

    @transaction.atomic
    def update(self, instance, validated_data: dict):
        name = next(iter(validated_data.keys()), '')
        serializer = CARRIER_MODEL_SERIALIZERS[name]
        settings = save_one_to_one_data(name, serializer, instance, payload=validated_data, partial=True)

        return getattr(settings, 'carrier_ptr', None)


ConnectionModelSerializer = type('ConnectionModelSerializer', (ConnectionModelSerializerBase,), {
    _name: _serializer(required=False)
    for _name, _serializer in CARRIER_MODEL_SERIALIZERS.items()
})

PartialConnectionModelSerializer = type('PartialConnectionModelSerializer', (ConnectionModelSerializerBase,), {
    _name: apply_optional_fields(_serializer)(required=False)
    for _name, _serializer in create_carrier_model_serializers(True).items()
})
