import typing
from django.db import transaction
from django.contrib.auth import get_user_model

import karrio.server.serializers as serializers
import karrio.server.core.validators as validators
import karrio.server.providers.models as providers
import karrio.server.manager.models as manager
import karrio.server.graph.models as graph


class UserModelSerializer(serializers.ModelSerializer):
    email = serializers.CharField(required=False)

    class Meta:
        model = get_user_model()
        extra_kwargs = {
            field: {"read_only": True}
            for field in ["id", "is_staff", "last_login", "date_joined"]
        }
        fields = [
            "email",
            "full_name",
            "is_active",
            "is_staff",
            "last_login",
            "date_joined",
        ]

    @transaction.atomic
    def update(self, instance, data: dict, **kwargs):
        user = super().update(instance, data)

        if data.get("is_active") == False:
            user.save(update_fields=["is_active"])

        return user


@serializers.owned_model_serializer
class AddressModelSerializer(
    validators.AugmentedAddressSerializer, serializers.ModelSerializer
):
    country_code = serializers.CharField(required=False)

    class Meta:
        model = manager.Address
        extra_kwargs = {field: {"read_only": True} for field in ["id", "validation"]}
        exclude = ["created_at", "updated_at", "created_by", "validation"]


@serializers.owned_model_serializer
class CommodityModelSerializer(serializers.ModelSerializer):
    weight_unit = serializers.CharField()
    value_currency = serializers.CharField(required=False)
    origin_country = serializers.CharField(required=False)

    class Meta:
        model = manager.Commodity
        exclude = ["created_at", "updated_at", "created_by", "parent"]
        extra_kwargs = {field: {"read_only": True} for field in ["id", "parent"]}


@serializers.owned_model_serializer
class CustomsModelSerializer(serializers.ModelSerializer):
    NESTED_FIELDS = ["commodities"]

    incoterm = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    commodities = serializers.make_fields_optional(CommodityModelSerializer)(
        many=True, allow_null=True, required=False
    )

    class Meta:
        model = manager.Customs
        exclude = ["created_at", "updated_at", "created_by"]
        extra_kwargs = {field: {"read_only": True} for field in ["id"]}

    @transaction.atomic
    def create(self, validated_data: dict, context: dict):
        data = {
            name: value
            for name, value in validated_data.items()
            if name not in self.NESTED_FIELDS
        }

        instance = super().create(data)

        serializers.save_many_to_many_data(
            "commodities",
            CommodityModelSerializer,
            instance,
            payload=validated_data,
            context=context,
        )

        return instance

    @transaction.atomic
    def update(
        self, instance: manager.Customs, validated_data: dict, **kwargs
    ) -> manager.Customs:
        data = {
            name: value
            for name, value in validated_data.items()
            if name not in self.NESTED_FIELDS
        }

        return super().update(instance, data)


@serializers.owned_model_serializer
class ParcelModelSerializer(validators.PresetSerializer, serializers.ModelSerializer):
    weight_unit = serializers.CharField(
        required=False, allow_null=True, allow_blank=True
    )
    dimension_unit = serializers.CharField(
        required=False, allow_null=True, allow_blank=True
    )

    class Meta:
        model = manager.Parcel
        exclude = ["created_at", "updated_at", "created_by", "items"]
        extra_kwargs = {field: {"read_only": True} for field in ["id"]}


@serializers.owned_model_serializer
class TemplateModelSerializer(serializers.ModelSerializer):
    address = serializers.make_fields_optional(AddressModelSerializer)(required=False)
    customs = serializers.make_fields_optional(CustomsModelSerializer)(required=False)
    parcel = serializers.make_fields_optional(ParcelModelSerializer)(required=False)

    class Meta:
        model = graph.Template
        exclude = ["created_at", "updated_at", "created_by"]
        extra_kwargs = {field: {"read_only": True} for field in ["id"]}

    @transaction.atomic
    def create(self, validated_data: dict, context: dict, **kwargs) -> graph.Template:
        data = {
            **validated_data,
            "address": serializers.save_one_to_one_data(
                "address",
                AddressModelSerializer,
                payload=validated_data,
                context=context,
            ),
            "customs": serializers.save_one_to_one_data(
                "customs",
                CustomsModelSerializer,
                payload=validated_data,
                context=context,
            ),
            "parcel": serializers.save_one_to_one_data(
                "parcel", ParcelModelSerializer, payload=validated_data, context=context
            ),
        }

        ensure_unique_default_related_data(validated_data, context=context)

        return super().create(data)

    @transaction.atomic
    def update(
        self, instance: graph.Template, validated_data: dict, **kwargs
    ) -> graph.Template:
        data = {
            key: value
            for key, value in validated_data.items()
            if key not in ["address", "customs", "parcel"]
        }

        serializers.save_one_to_one_data(
            "address", AddressModelSerializer, instance, payload=validated_data
        )
        serializers.save_one_to_one_data(
            "customs", CustomsModelSerializer, instance, payload=validated_data
        )
        serializers.save_one_to_one_data(
            "parcel", ParcelModelSerializer, instance, payload=validated_data
        )

        ensure_unique_default_related_data(validated_data, instance)

        return super().update(instance, data)


def ensure_unique_default_related_data(
    data: dict = None, instance: typing.Optional[graph.Template] = None, context=None
):
    _get = lambda key: data.get(key, getattr(instance, key, None))
    if _get("is_default") is not True:
        return

    if _get("address") is not None:
        query = dict(address__isnull=False, is_default=True)
    elif _get("customs") is not None:
        query = dict(customs__isnull=False, is_default=True)
    elif _get("parcel") is not None:
        query = dict(parcel__isnull=False, is_default=True)
    else:
        return

    graph.Template.access_by(context or instance.created_by).exclude(
        id=_get("id")
    ).filter(**query).update(is_default=False)


@serializers.owned_model_serializer
class ServiceLevelModelSerializer(serializers.ModelSerializer):
    dimension_unit = serializers.CharField(
        required=False, allow_null=True, allow_blank=True
    )
    weight_unit = serializers.CharField(
        required=False, allow_null=True, allow_blank=True
    )
    currency = serializers.CharField(required=False, allow_null=True, allow_blank=True)

    class Meta:
        model = providers.ServiceLevel
        exclude = ["created_at", "updated_at", "created_by"]
        extra_kwargs = {field: {"read_only": True} for field in ["id"]}


@serializers.owned_model_serializer
class LabelTemplateModelSerializer(serializers.ModelSerializer):
    template_type = serializers.CharField(required=False)

    class Meta:
        model = providers.LabelTemplate
        exclude = ["created_at", "updated_at", "created_by"]
        extra_kwargs = {field: {"read_only": True} for field in ["id"]}


def create_carrier_model_serializers(partial: bool = False):
    def _create_model_serializer(carrier_name: str, carrier_model):
        _name = carrier_name
        _extra_fields: dict = {}

        if hasattr(carrier_model, "account_country_code"):
            _extra_fields.update(
                account_country_code=serializers.CharField(required=False, allow_null=True)
            )

        if hasattr(carrier_model, "services"):
            _service_serializer = (
                serializers.make_fields_optional(ServiceLevelModelSerializer)
                if partial
                else serializers.exclude_id_field(ServiceLevelModelSerializer)
            )
            _extra_fields.update(
                services=_service_serializer(many=True, allow_null=True, required=False)
            )

        if hasattr(carrier_model, "label_template"):
            _template_serializer = (
                serializers.make_fields_optional(LabelTemplateModelSerializer)
                if partial
                else LabelTemplateModelSerializer
            )
            _extra_fields.update(
                label_template=_template_serializer(allow_null=True, required=False)
            )

        class Meta:
            model = carrier_model
            extra_kwargs = {field: {"read_only": True} for field in ["id"]}
            exclude = (
                "created_at",
                "updated_at",
                "created_by",
                "capabilities",
                "active_users",
            )

        return serializers.owned_model_serializer(
            type(
                _name,
                (serializers.ModelSerializer,),
                {
                    "Meta": Meta,
                    "carrier_id": serializers.CharField(required=not partial),
                    **_extra_fields,
                },
            )
        )

    return {
        name: _create_model_serializer(name, model)
        for name, model in providers.MODELS.items()
    }


CARRIER_MODEL_SERIALIZERS = create_carrier_model_serializers()
PARTIAL_CARRIER_MODEL_SERIALIZERS = create_carrier_model_serializers(True)


@serializers.owned_model_serializer
class ConnectionModelSerializerBase(serializers.ModelSerializer):
    class Meta:
        model = providers.Carrier
        exclude = [
            "created_at",
            "updated_at",
            "created_by",
            "carrier_id",
            "test_mode",
            "active",
            "capabilities",
            "active_users",
        ]

    @transaction.atomic
    def create(self, validated_data: dict, context: serializers.Context, **kwargs):
        name = next(
            (k for k in validated_data.keys() if k in CARRIER_MODEL_SERIALIZERS.keys()),
            "",
        )
        settings_data = validated_data.get(name, {})
        serializer = CARRIER_MODEL_SERIALIZERS.get(name)
        settings_name = serializer.Meta.model.__name__.lower()

        payload = {
            key: value
            for key, value in settings_data.items()
            if key not in ["id", "services", "label_template"]
        }
        label_template = serializers.save_one_to_one_data(
            "label_template",
            LabelTemplateModelSerializer,
            payload=settings_data,
            context=context,
        )
        settings = serializers.save_one_to_one_data(
            settings_name,
            serializer,
            payload={settings_name: payload},
            context=context,
        )

        services = settings_data.get("services") or getattr(
            settings, "default_services", []
        )
        if any(services):
            serializers.save_many_to_many_data(
                "services",
                ServiceLevelModelSerializer,
                settings,
                payload=dict(services=services),
                context=context,
            )
        if label_template:
            settings.label_template = label_template
            settings.save()

        return getattr(settings, "carrier_ptr", None)

    @transaction.atomic
    def update(
        self, instance, validated_data: dict, context: serializers.Context, **kwargs
    ):
        carrier_name = (
            instance.settings.carrier_name
            if instance.settings.carrier_name in providers.MODELS
            else "generic"
        )
        settings_name = instance.settings.__class__.__name__.lower()
        serializer = CARRIER_MODEL_SERIALIZERS.get(carrier_name)

        payload = {
            key: value
            for key, value in validated_data.get(carrier_name, {}).items()
            if key not in ["id", "services", "label_template"]
        }

        settings = serializers.save_one_to_one_data(
            settings_name,
            serializer,
            instance,
            payload={settings_name: payload},
            context=context,
        )

        template = validated_data.get(carrier_name, {}).get("label_template")

        if template:
            settings.label_template = serializers.save_one_to_one_data(
                "label_template",
                LabelTemplateModelSerializer,
                settings,
                payload=dict(label_template=template),
                context=context,
            )
            settings.save()

        return getattr(settings, "carrier_ptr", instance)


ConnectionModelSerializer = type(
    "ConnectionModelSerializer",
    (serializers.exclude_id_field(ConnectionModelSerializerBase),),
    {
        _name: _serializer(required=False)
        for _name, _serializer in CARRIER_MODEL_SERIALIZERS.items()
    },
)

PartialConnectionModelSerializer = type(
    "PartialConnectionModelSerializer",
    (ConnectionModelSerializerBase,),
    {
        _name: serializers.make_fields_optional(_serializer)(required=False)
        for _name, _serializer in PARTIAL_CARRIER_MODEL_SERIALIZERS.items()
    },
)
