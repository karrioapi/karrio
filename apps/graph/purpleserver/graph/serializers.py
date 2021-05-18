import typing
from django.db import transaction
from django.contrib.auth import get_user_model

from purplship.core.utils import DP
from purpleserver.serializers import (
    ModelSerializer, Serializer, save_one_to_one_data, save_many_to_many_data, owned_model_serializer, Context
)
import purpleserver.core.serializers as serializers
import purpleserver.core.validators as validators
import purpleserver.providers.models as providers
import purpleserver.manager.models as manager
import purpleserver.graph.models as graph

User = get_user_model()


def apply_optional_fields(serializer: typing.Type[ModelSerializer]):
    _name = f"Partial{serializer.__name__}"

    class _Meta(serializer.Meta):
        extra_kwargs = {
            **getattr(serializer.Meta, 'extra_kwargs', {}),
            **{field.name: {'required': False} for field in serializer.Meta.model._meta.fields}
        }

    return type(_name, (serializer,), dict(Meta=_Meta))


class UserModelSerializer(ModelSerializer):
    email = serializers.CharField(required=False)

    class Meta:
        model = User
        extra_kwargs = {
            field: {'read_only': True} for field in ['is_staff', 'last_login', 'date_joined']
        }
        fields = ['email', 'full_name', 'is_active', 'is_staff', 'last_login', 'date_joined']


@owned_model_serializer
class AddressModelSerializer(validators.AugmentedAddressSerializer, ModelSerializer):
    country_code = serializers.CharField(required=False)

    class Meta:
        model = manager.Address
        extra_kwargs = {
            **{key: {'required': True} for key in ['country_code']},
            **{key: {'read_only': False} for key in ['validate_location', 'validation']},
        }
        exclude = ['created_at', 'updated_at', 'created_by']


@owned_model_serializer
class CommodityModelSerializer(ModelSerializer):
    weight_unit = serializers.CharField()

    class Meta:
        model = manager.Commodity
        exclude = ['created_at', 'updated_at', 'created_by']


@owned_model_serializer
class CustomsModelSerializer(ModelSerializer):
    NESTED_FIELDS = ['commodities']

    commodities = apply_optional_fields(CommodityModelSerializer)(many=True, allow_null=True, required=False)

    class Meta:
        model = manager.Customs
        exclude = ['created_at', 'updated_at', 'created_by', 'options']

    @transaction.atomic
    def create(self, validated_data: dict, context: dict):
        data = {
            **{name: value for name, value in validated_data.items() if name not in self.NESTED_FIELDS},
            'options': DP.to_dict(validated_data['options']) if 'options' in validated_data else None,
            'duty': DP.to_dict(validated_data['duty']) if 'duty' in validated_data else None
        }

        instance = super().create(data)

        save_many_to_many_data(
            'commodities', CommodityModelSerializer, instance, payload=validated_data, context=context)

        return instance

    @transaction.atomic
    def update(self, instance: manager.Customs, validated_data: dict, **kwargs) -> manager.Customs:
        data = {
            **{name: value for name, value in validated_data.items() if name not in self.NESTED_FIELDS},
            'options': DP.to_dict(validated_data['options']) if 'options' in validated_data else instance.options,
            'duty': DP.to_dict(validated_data['duty']) if 'duty' in validated_data else instance.duty
        }

        return super().update(instance, data)


@owned_model_serializer
class ParcelModelSerializer(validators.PresetSerializer, ModelSerializer):
    class Meta:
        model = manager.Parcel
        exclude = ['created_at', 'updated_at', 'created_by']


@owned_model_serializer
class TemplateModelSerializer(ModelSerializer):
    address = apply_optional_fields(AddressModelSerializer)(required=False)
    customs = apply_optional_fields(CustomsModelSerializer)(required=False)
    parcel = apply_optional_fields(ParcelModelSerializer)(required=False)

    class Meta:
        model = graph.Template
        exclude = ['created_at', 'updated_at', 'created_by']

    @transaction.atomic
    def create(self, validated_data: dict, context: dict, **kwargs) -> graph.Template:
        data = {
            **validated_data,
            'address': save_one_to_one_data('address', AddressModelSerializer, payload=validated_data, context=context),
            'customs': save_one_to_one_data('customs', CustomsModelSerializer, payload=validated_data, context=context),
            'parcel': save_one_to_one_data('parcel', ParcelModelSerializer, payload=validated_data, context=context)
        }

        ensure_unique_default_related_data(validated_data, context=context)

        return super().create(data)

    @transaction.atomic
    def update(self, instance: graph.Template, validated_data: dict, **kwargs) -> graph.Template:
        data = {key: value for key, value in validated_data.items() if key not in ['address', 'customs', 'parcel']}

        save_one_to_one_data('address', AddressModelSerializer, instance, payload=validated_data)
        save_one_to_one_data('customs', CustomsModelSerializer, instance, payload=validated_data)
        save_one_to_one_data('parcel', ParcelModelSerializer, instance, payload=validated_data)

        ensure_unique_default_related_data(validated_data, instance)

        return super().update(instance, data)


def ensure_unique_default_related_data(
        data: dict = None, instance: typing.Optional[graph.Template] = None, context = None):

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

    default_templates = graph.Template.access_by(context or instance.created_by).filter(**query)
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

        return owned_model_serializer(type(_name, (ModelSerializer,), dict(
            Meta=Meta,
            carrier_id=serializers.CharField(required=not partial)
        )))

    return {
        carrier.__name__.lower(): _create_model_serializer(carrier)
        for carrier in providers.MODELS.values()
    }


CARRIER_MODEL_SERIALIZERS = create_carrier_model_serializers()


@owned_model_serializer
class ConnectionModelSerializerBase(ModelSerializer):
    class Meta:
        model = providers.Carrier
        exclude = ['created_at', 'updated_at', 'created_by', 'carrier_id', 'test', 'active']

    @transaction.atomic
    def create(self, validated_data: dict, context: dict, **kwargs):
        name = next((k for k in validated_data.keys() if 'settings' in k), '')
        serializer = CARRIER_MODEL_SERIALIZERS.get(name)
        settings = save_one_to_one_data(name, serializer, payload=validated_data, context=context)

        return getattr(settings, 'carrier_ptr', None)

    @transaction.atomic
    def update(self, instance, validated_data: dict, **kwargs):
        name = next((k for k in validated_data.keys() if 'settings' in k), '')
        serializer = CARRIER_MODEL_SERIALIZERS.get(name)
        settings = save_one_to_one_data(name, serializer, instance, payload=validated_data)

        return getattr(settings, 'carrier_ptr', None)


ConnectionModelSerializer = type('ConnectionModelSerializer', (ConnectionModelSerializerBase,), {
    _name: _serializer(required=False)
    for _name, _serializer in CARRIER_MODEL_SERIALIZERS.items()
})

PartialConnectionModelSerializer = type('PartialConnectionModelSerializer', (ConnectionModelSerializerBase,), {
    _name: apply_optional_fields(_serializer)(required=False)
    for _name, _serializer in create_carrier_model_serializers(True).items()
})
