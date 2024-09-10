import typing
from django.db import transaction
from django.contrib.auth import get_user_model

import karrio.server.serializers as serializers
import karrio.server.core.validators as validators
import karrio.server.providers.models as providers
import karrio.server.manager.models as manager
import karrio.server.graph.models as graph
import karrio.server.core.models as core
import karrio.server.user.models as auth


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
class WorkspaceConfigModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = auth.WorkspaceConfig
        extra_kwargs = {field: {"read_only": True} for field in ["id"]}
        exclude = ["created_at", "updated_at", "created_by"]

    def create(
        self, validated_data: dict, context: serializers.Context = None, **kwargs
    ):
        instance = super().create(validated_data, context=context, **kwargs)

        if (
            hasattr(auth.WorkspaceConfig, "org")
            and getattr(context, "org", None) is not None
        ):
            context.org.config = instance
            context.org.save()

        return instance


@serializers.owned_model_serializer
class MetafieldModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = core.Metafield
        extra_kwargs = {field: {"read_only": True} for field in ["id"]}
        exclude = ["created_at", "updated_at", "created_by"]


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


@serializers.owned_model_serializer
class RateSheetModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = providers.RateSheet
        exclude = ["created_at", "updated_at", "created_by"]
        extra_kwargs = {field: {"read_only": True} for field in ["id", "services"]}
