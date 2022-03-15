import typing
from django.db import transaction
from django.conf import settings
from django.contrib.auth import get_user_model

from karrio.server.serializers import (
    ModelSerializer,
    save_one_to_one_data,
    save_many_to_many_data,
    owned_model_serializer,
    make_fields_optional,
    exclude_id_field,
    Context,
)
import karrio.server.core.serializers as serializers
import karrio.server.core.validators as validators
import karrio.server.providers.models as providers
import karrio.server.manager.models as manager
import karrio.server.graph.models as graph


class UserModelSerializer(ModelSerializer):
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


@owned_model_serializer
class AddressModelSerializer(validators.AugmentedAddressSerializer, ModelSerializer):
    country_code = serializers.CharField(required=False)

    class Meta:
        model = manager.Address
        extra_kwargs = {field: {"read_only": True} for field in ["id", "validation"]}
        exclude = ["created_at", "updated_at", "created_by", "validation"]


@owned_model_serializer
class CommodityModelSerializer(ModelSerializer):
    weight_unit = serializers.CharField()
    value_currency = serializers.CharField(required=False)
    origin_country = serializers.CharField(required=False)

    class Meta:
        model = manager.Commodity
        exclude = ["created_at", "updated_at", "created_by", "parent"]
        extra_kwargs = {field: {"read_only": True} for field in ["id", "parent"]}


@owned_model_serializer
class CustomsModelSerializer(ModelSerializer):
    NESTED_FIELDS = ["commodities"]

    incoterm = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    commodities = make_fields_optional(CommodityModelSerializer)(
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

        save_many_to_many_data(
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


@owned_model_serializer
class ParcelModelSerializer(validators.PresetSerializer, ModelSerializer):
    weight_unit = serializers.CharField(
        required=False, allow_null=True, allow_blank=True
    )
    dimension_unit = serializers.CharField(
        required=False, allow_null=True, allow_blank=True
    )

    class Meta:
        model = manager.Parcel
        exclude = ["created_at", "updated_at", "created_by"]
        extra_kwargs = {field: {"read_only": True} for field in ["id"]}


@owned_model_serializer
class TemplateModelSerializer(ModelSerializer):
    address = make_fields_optional(AddressModelSerializer)(required=False)
    customs = make_fields_optional(CustomsModelSerializer)(required=False)
    parcel = make_fields_optional(ParcelModelSerializer)(required=False)

    class Meta:
        model = graph.Template
        exclude = ["created_at", "updated_at", "created_by"]
        extra_kwargs = {field: {"read_only": True} for field in ["id"]}

    @transaction.atomic
    def create(self, validated_data: dict, context: dict, **kwargs) -> graph.Template:
        data = {
            **validated_data,
            "address": save_one_to_one_data(
                "address",
                AddressModelSerializer,
                payload=validated_data,
                context=context,
            ),
            "customs": save_one_to_one_data(
                "customs",
                CustomsModelSerializer,
                payload=validated_data,
                context=context,
            ),
            "parcel": save_one_to_one_data(
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

        save_one_to_one_data(
            "address", AddressModelSerializer, instance, payload=validated_data
        )
        save_one_to_one_data(
            "customs", CustomsModelSerializer, instance, payload=validated_data
        )
        save_one_to_one_data(
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


@owned_model_serializer
class ServiceLevelModelSerializer(ModelSerializer):
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


@owned_model_serializer
class LabelTemplateModelSerializer(ModelSerializer):
    template_type = serializers.CharField(required=False)

    class Meta:
        model = providers.LabelTemplate
        exclude = ["created_at", "updated_at", "created_by"]
        extra_kwargs = {field: {"read_only": True} for field in ["id"]}


def create_carrier_model_serializers(partial: bool = False):
    def _create_model_serializer(carrier_model):
        _name = f"{carrier_model.__name__}"
        _extra_fields = {}
        _extra_exclude = []

        if hasattr(carrier_model, "account_country_code"):
            required = (
                False
                if partial
                else not (
                    carrier_model.account_country_code.field.blank
                    or carrier_model.account_country_code.field.null
                )
            )
            _extra_fields.update(
                account_country_code=serializers.CharField(required=required)
            )

        if hasattr(carrier_model, "services"):
            _service_serializer = (
                make_fields_optional(ServiceLevelModelSerializer)
                if partial
                else exclude_id_field(ServiceLevelModelSerializer)
            )
            _extra_fields.update(
                services=_service_serializer(many=True, allow_null=True, required=False)
            )

        if hasattr(carrier_model, "label_template"):
            _template_serializer = (
                make_fields_optional(LabelTemplateModelSerializer)
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
                *_extra_exclude,
            )

        return owned_model_serializer(
            type(
                _name,
                (ModelSerializer,),
                {
                    "Meta": Meta,
                    "carrier_id": serializers.CharField(required=not partial),
                    **_extra_fields,
                },
            )
        )

    return {
        carrier.__name__.lower(): _create_model_serializer(carrier)
        for carrier in providers.MODELS.values()
    }


CARRIER_MODEL_SERIALIZERS = create_carrier_model_serializers()


@owned_model_serializer
class ConnectionModelSerializerBase(ModelSerializer):
    class Meta:
        model = providers.Carrier
        extra_kwargs = {field: {"read_only": True} for field in ["id"]}
        exclude = [
            "created_at",
            "updated_at",
            "created_by",
            "carrier_id",
            "test",
            "active",
            "capabilities",
            "active_users",
        ]

    @transaction.atomic
    def create(self, validated_data: dict, context: Context, **kwargs):
        name = next((k for k in validated_data.keys() if "settings" in k), "")
        serializer = CARRIER_MODEL_SERIALIZERS.get(name)
        settings_data = validated_data.get(name, {})
        payload = {
            key: value
            for key, value in settings_data.items()
            if key not in ["id", "services", "label_template"]
        }
        label_template = save_one_to_one_data(
            "label_template",
            LabelTemplateModelSerializer,
            payload=settings_data,
            context=context,
        )

        settings = save_one_to_one_data(
            name, serializer, payload={name: payload}, context=context
        )

        services = settings_data.get("services") or getattr(
            settings, "default_services", []
        )
        if any(services):
            save_many_to_many_data(
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
    def update(self, instance, validated_data: dict, context: Context, **kwargs):
        name = next((k for k in validated_data.keys() if "settings" in k), "")
        serializer = CARRIER_MODEL_SERIALIZERS.get(name)

        payload = {
            key: value
            for key, value in validated_data.get(name, {}).items()
            if key not in ["id", "services", "label_template"]
        }

        settings = save_one_to_one_data(
            name, serializer, instance, payload={name: payload}
        )

        template = validated_data.get(name, {}).get("label_template")
        if template:
            settings.label_template = save_one_to_one_data(
                "label_template",
                LabelTemplateModelSerializer,
                settings,
                payload=dict(label_template=template),
                context=context,
            )
            settings.save()

        return getattr(settings, "carrier_ptr", None)


ConnectionModelSerializer = type(
    "ConnectionModelSerializer",
    (exclude_id_field(ConnectionModelSerializerBase),),
    {
        _name: _serializer(required=False)
        for _name, _serializer in CARRIER_MODEL_SERIALIZERS.items()
    },
)

PartialConnectionModelSerializer = type(
    "PartialConnectionModelSerializer",
    (ConnectionModelSerializerBase,),
    {
        _name: make_fields_optional(_serializer)(required=False)
        for _name, _serializer in create_carrier_model_serializers(True).items()
    },
)
