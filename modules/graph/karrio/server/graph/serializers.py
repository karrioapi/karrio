import typing
import strawberry
from django.db import transaction
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from rest_framework import exceptions

import karrio.server.serializers as serializers
import karrio.server.core.validators as validators
import karrio.server.providers.models as providers
import karrio.server.manager.models as manager
import karrio.server.graph.models as graph
import karrio.server.core.models as core
import karrio.server.user.models as auth
import karrio.server.core.gateway as gateway


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
            "metadata",
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
    object_type = serializers.CharField(required=False, allow_null=True)
    object_id = serializers.CharField(required=False, allow_null=True)

    class Meta:
        model = core.Metafield
        extra_kwargs = {field: {"read_only": True} for field in ["id"]}
        exclude = ["created_at", "updated_at", "created_by", "content_type"]

    def validate(self, data):
        from django.contrib.contenttypes.models import ContentType

        object_type = data.pop("object_type", None)
        object_id = data.get("object_id")

        if object_type and object_id:
            ct = ContentType.objects.filter(model=object_type).first()
            if not ct:
                raise serializers.ValidationError(
                    {"object_type": f"Invalid object type: {object_type}"}
                )
            data["content_type"] = ct
        elif object_type or object_id:
            raise serializers.ValidationError(
                "Both object_type and object_id must be provided together"
            )

        return data


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
            if key not in ["address", "parcel"]
        }

        serializers.save_one_to_one_data(
            "address", AddressModelSerializer, instance, payload=validated_data
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
    """
    Serializer for ServiceLevel model.

    Services reference shared zones and surcharges at the RateSheet level
    via zone_ids and surcharge_ids.
    """

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

    def update_services(
        self, services_data: list, remove_missing: bool = False
    ) -> None:
        """Update services of the rate sheet."""
        existing_services = {s.id: s for s in self.instance.services.all()}

        for service_data in services_data:
            service_id = service_data.get("id")
            if service_id and service_id in existing_services:
                # Update existing service
                service = existing_services[service_id]
                service_serializer = ServiceLevelModelSerializer(
                    service,
                    data=service_data,
                    context=self.context,
                    partial=True,
                )
                service_serializer.is_valid(raise_exception=True)
                service_serializer.save()
            else:
                # Create new service
                service_serializer = ServiceLevelModelSerializer(
                    data=service_data,
                    context=self.context,
                )
                service_serializer.is_valid(raise_exception=True)
                service = service_serializer.save()
                self.instance.services.add(service)

        # Remove services that are not in the update
        if remove_missing:
            service_ids = {s.get("id") for s in services_data if "id" in s}
            for service in existing_services.values():
                if service.id not in service_ids:
                    self.instance.services.remove(service)
                    service.delete()

    def update_carriers(self, carriers: list) -> None:
        """Update carrier associations."""
        if carriers is not None:
            _ids = set(
                [*carriers, *(self.instance.carriers.values_list("id", flat=True))]
            )
            _carriers = gateway.Carriers.list(
                context=self.context,
                carrier_name=self.instance.carrier_name,
            ).filter(id__in=list(_ids))

            for carrier in _carriers:
                carrier.rate_sheet = self.instance if carrier.id in carriers else None
                carrier.save(update_fields=["rate_sheet"])

    def process_zones(self, zones_data: list, remove_missing: bool = False) -> None:
        """Process zones for the rate sheet.

        Args:
            zones_data: List of zone dicts with id, label, country_codes, etc.
            remove_missing: If True, remove zones not present in zones_data.
        """
        existing_zone_ids = {z["id"] for z in (self.instance.zones or [])}
        incoming_zone_ids = set()

        for zone_data in zones_data:
            zone_dict = {k: v for k, v in zone_data.items() if v is not None}
            zone_id = zone_dict.get("id")

            if zone_id:
                incoming_zone_ids.add(zone_id)

            if zone_id and zone_id in existing_zone_ids:
                self.instance.update_zone(zone_id, zone_dict)
            else:
                self.instance.add_zone(zone_dict)

        # Remove zones not in incoming data
        if remove_missing:
            zones_to_remove = existing_zone_ids - incoming_zone_ids
            for zone_id in zones_to_remove:
                self.instance.remove_zone(zone_id)

    def process_surcharges(self, surcharges_data: list, remove_missing: bool = False) -> None:
        """Process surcharges for the rate sheet.

        Args:
            surcharges_data: List of surcharge dicts with id, name, amount, etc.
            remove_missing: If True, remove surcharges not present in surcharges_data.
        """
        existing_surcharge_ids = {s["id"] for s in (self.instance.surcharges or [])}
        incoming_surcharge_ids = set()

        for surcharge_data in surcharges_data:
            surcharge_dict = {k: v for k, v in surcharge_data.items() if v is not None}
            surcharge_id = surcharge_dict.get("id")

            if surcharge_id:
                incoming_surcharge_ids.add(surcharge_id)

            if surcharge_id and surcharge_id in existing_surcharge_ids:
                self.instance.update_surcharge(surcharge_id, surcharge_dict)
            else:
                self.instance.add_surcharge(surcharge_dict)

        # Remove surcharges not in incoming data
        if remove_missing:
            surcharges_to_remove = existing_surcharge_ids - incoming_surcharge_ids
            for surcharge_id in surcharges_to_remove:
                self.instance.remove_surcharge(surcharge_id)

    def process_service_rates(
        self, service_rates_data: list, temp_to_real_id_map: dict = None
    ) -> None:
        """Process service rates for the rate sheet.

        Args:
            service_rates_data: List of service rate dicts with service_id, zone_id, rate, etc.
            temp_to_real_id_map: Optional mapping of temp-{idx} IDs to real service IDs.
        """
        temp_to_real_id_map = temp_to_real_id_map or {}

        for rate_data in service_rates_data:
            rate_dict = {k: v for k, v in rate_data.items() if v is not None}
            service_id = rate_dict.pop("service_id", None)
            zone_id = rate_dict.pop("zone_id", None)

            # Map temp service ID to real ID if needed
            if service_id and str(service_id).startswith("temp-"):
                service_id = temp_to_real_id_map.get(service_id, service_id)

            if service_id and zone_id:
                self.instance.update_service_rate(service_id, zone_id, rate_dict)

    def build_temp_to_real_service_map(self, services_data: list) -> dict:
        """Build mapping from temp-{idx} IDs to real service IDs by service_code."""
        created_services = {s.service_code: s.id for s in self.instance.services.all()}

        return {
            f"temp-{idx}": created_services[svc.get("service_code")]
            for idx, svc in enumerate(services_data)
            if svc.get("service_code") in created_services
        }

    def update(self, instance, validated_data, **kwargs):
        """Handle updates of rate sheet data including services and carriers.

        When zones or surcharges data is provided, it's treated as a full replacement -
        zones/surcharges not in the incoming data will be removed.
        """
        services_data = validated_data.pop("services", None)
        carriers = (
            validated_data.pop("carriers", None)
            if "carriers" in validated_data
            else None
        )
        zones_data = validated_data.pop("zones", None)
        surcharges_data = validated_data.pop("surcharges", None)
        service_rates_data = validated_data.pop("service_rates", None)
        remove_missing_services = validated_data.pop("remove_missing_services", False)

        instance = super().update(instance, validated_data)

        if services_data is not None:
            self.update_services(services_data, remove_missing_services)

        if carriers is not None:
            self.update_carriers(carriers)

        if zones_data:
            # Full update: remove zones not present in incoming data
            self.process_zones(zones_data, remove_missing=True)

        if surcharges_data:
            # Full update: remove surcharges not present in incoming data
            self.process_surcharges(surcharges_data, remove_missing=True)

        if service_rates_data:
            self.process_service_rates(service_rates_data)

        return instance
