import karrio.server.core.gateway as gateway
import karrio.server.core.models as core
import karrio.server.core.validators as validators
import karrio.server.graph.models as graph
import karrio.server.manager.models as manager
import karrio.server.providers.models as providers
import karrio.server.serializers as serializers
import karrio.server.user.models as auth
from django.contrib.auth import get_user_model
from django.db import transaction


class UserModelSerializer(serializers.ModelSerializer):
    email = serializers.CharField(required=False)

    class Meta:
        model = get_user_model()
        extra_kwargs = {field: {"read_only": True} for field in ["id", "is_staff", "last_login", "date_joined"]}
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

        if not data.get("is_active"):
            user.save(update_fields=["is_active"])

        return user


@serializers.owned_model_serializer
class WorkspaceConfigModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = auth.WorkspaceConfig
        extra_kwargs = {field: {"read_only": True} for field in ["id"]}
        exclude = ["created_at", "updated_at", "created_by"]

    def create(self, validated_data: dict, context: serializers.Context = None, **kwargs):
        instance = super().create(validated_data, context=context, **kwargs)

        if hasattr(auth.WorkspaceConfig, "org") and getattr(context, "org", None) is not None:
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
                raise serializers.ValidationError({"object_type": f"Invalid object type: {object_type}"})
            data["content_type"] = ct
        elif object_type or object_id:
            raise serializers.ValidationError("Both object_type and object_id must be provided together")

        return data


@serializers.owned_model_serializer
class AddressModelSerializer(validators.AugmentedAddressSerializer, serializers.ModelSerializer):
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
    weight_unit = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    dimension_unit = serializers.CharField(required=False, allow_null=True, allow_blank=True)

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
    def update(self, instance: graph.Template, validated_data: dict, **kwargs) -> graph.Template:
        data = {key: value for key, value in validated_data.items() if key not in ["address", "parcel"]}

        serializers.save_one_to_one_data("address", AddressModelSerializer, instance, payload=validated_data)
        serializers.save_one_to_one_data("parcel", ParcelModelSerializer, instance, payload=validated_data)

        ensure_unique_default_related_data(validated_data, instance)

        return super().update(instance, data)


def ensure_unique_default_related_data(data: dict = None, instance: graph.Template | None = None, context=None):
    def _get(key):
        return data.get(key, getattr(instance, key, None))

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

    graph.Template.access_by(context or instance.created_by).exclude(id=_get("id")).filter(**query).update(
        is_default=False
    )


@serializers.owned_model_serializer
class ServiceLevelModelSerializer(serializers.ModelSerializer):
    """
    Serializer for ServiceLevel model.

    Services reference shared zones and surcharges at the RateSheet level
    via zone_ids and surcharge_ids.
    """

    dimension_unit = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    weight_unit = serializers.CharField(required=False, allow_null=True, allow_blank=True)
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


class _RateSheetSerializerMixin:
    """Shared methods for account and system rate sheet serializers."""

    def update_services(self, services_data: list, remove_missing: bool = False) -> None:
        """Update services of the rate sheet using bulk operations.

        Collects all changes in memory, then:
        - bulk_update for modified services (1 query)
        - bulk_create for new services (1 query)
        - single M2M add for new services (1 query)
        """
        existing_services = {s.id: s for s in self.instance.services.all()}
        services_to_update = []
        update_fields = set()
        services_to_create = []

        for service_data in services_data:
            service_id = service_data.get("id")
            if service_id and service_id in existing_services:
                service = existing_services[service_id]
                changed = False
                for field, value in service_data.items():
                    if field == "id":
                        continue
                    if getattr(service, field, None) != value:
                        setattr(service, field, value)
                        update_fields.add(field)
                        changed = True
                if changed:
                    services_to_update.append(service)
            else:
                service_serializer = ServiceLevelModelSerializer(
                    data=service_data,
                    context=self.context,
                )
                service_serializer.is_valid(raise_exception=True)
                instance = providers.ServiceLevel(**service_serializer.validated_data)
                # Set created_by from context (required NOT NULL field)
                user = (
                    self.context.get("user") if isinstance(self.context, dict) else getattr(self.context, "user", None)
                )
                if user and not instance.created_by_id:
                    instance.created_by = user
                services_to_create.append(instance)

        # Bulk update existing services (1 query)
        if services_to_update and update_fields:
            providers.ServiceLevel.objects.bulk_update(services_to_update, list(update_fields))

        # Bulk create new services and add to M2M (2 queries)
        if services_to_create:
            created = providers.ServiceLevel.objects.bulk_create(services_to_create)
            self.instance.services.add(*created)

        # Remove services that are not in the update
        if remove_missing:
            service_ids = {s.get("id") for s in services_data if "id" in s}
            to_remove = [s for s in existing_services.values() if s.id not in service_ids]
            if to_remove:
                remove_ids = [s.id for s in to_remove]
                self.instance.services.remove(*to_remove)
                providers.ServiceLevel.objects.filter(id__in=remove_ids).delete()

    def update_carriers(self, carriers: list) -> None:
        """Update carrier associations using bulk queries instead of per-carrier saves."""
        if carriers is not None:
            carrier_qs = gateway.Carriers.list(
                context=self.context,
                carrier_name=self.instance.carrier_name,
            )
            # Link requested carriers (1 query)
            carrier_qs.filter(id__in=carriers).update(rate_sheet=self.instance)
            # Unlink carriers no longer associated (1 query)
            carrier_qs.filter(rate_sheet=self.instance).exclude(id__in=carriers).update(rate_sheet=None)

    def process_zones(self, zones_data: list, remove_missing: bool = False) -> None:
        """Process zones for the rate sheet.

        Batches all zone mutations in memory and writes once to avoid N+1 UPDATEs.

        Args:
            zones_data: List of zone dicts with id, label, country_codes, etc.
            remove_missing: If True, remove zones not present in zones_data.
        """
        zones = list(self.instance.zones or [])
        zone_map = {z["id"]: i for i, z in enumerate(zones) if z.get("id")}
        incoming_zone_ids = set()

        for zone_data in zones_data:
            zone_dict = {k: v for k, v in zone_data.items() if v is not None}
            zone_id = zone_dict.get("id")

            if zone_id:
                incoming_zone_ids.add(zone_id)

            if zone_id and zone_id in zone_map:
                # Update existing zone in memory
                idx = zone_map[zone_id]
                zones[idx] = {"id": zone_id, **{k: v for k, v in zone_dict.items() if k != "id"}}
            else:
                # Add new zone in memory
                if not zone_id:
                    zone_dict["id"] = f"zone_{len(zones) + 1}"
                zones.append(zone_dict)
                zone_map[zone_dict["id"]] = len(zones) - 1

        # Remove zones not in incoming data
        if remove_missing:
            zones = [z for z in zones if z.get("id") in incoming_zone_ids]

        # Single write for all zone mutations
        self.instance.zones = zones
        self.instance.save(update_fields=["zones"])

    def process_surcharges(self, surcharges_data: list, remove_missing: bool = False) -> None:
        """Process surcharges for the rate sheet.

        Batches all surcharge mutations in memory and writes once to avoid N+1 UPDATEs.

        Args:
            surcharges_data: List of surcharge dicts with id, name, amount, etc.
            remove_missing: If True, remove surcharges not present in surcharges_data.
        """
        surcharges = list(self.instance.surcharges or [])
        surcharge_map = {s["id"]: i for i, s in enumerate(surcharges) if s.get("id")}
        incoming_surcharge_ids = set()

        for surcharge_data in surcharges_data:
            surcharge_dict = {k: v for k, v in surcharge_data.items() if v is not None}
            surcharge_id = surcharge_dict.get("id")

            if surcharge_id:
                incoming_surcharge_ids.add(surcharge_id)

            if surcharge_id and surcharge_id in surcharge_map:
                # Update existing surcharge in memory
                idx = surcharge_map[surcharge_id]
                surcharges[idx] = {"id": surcharge_id, **{k: v for k, v in surcharge_dict.items() if k != "id"}}
            else:
                # Add new surcharge in memory
                if not surcharge_id:
                    surcharge_dict["id"] = f"surch_{len(surcharges) + 1}"
                surcharge_dict.setdefault("active", True)
                surcharge_dict.setdefault("surcharge_type", "fixed")
                surcharges.append(surcharge_dict)
                surcharge_map[surcharge_dict["id"]] = len(surcharges) - 1

        # Remove surcharges not in incoming data
        if remove_missing:
            surcharges = [s for s in surcharges if s.get("id") in incoming_surcharge_ids]

        # Single write for all surcharge mutations
        self.instance.surcharges = surcharges
        self.instance.save(update_fields=["surcharges"])

    def process_service_rates(self, service_rates_data: list, temp_to_real_id_map: dict = None) -> None:
        """Process service rates for the rate sheet.

        Uses batch_update_service_rates() to avoid the single-entry fallback
        in update_service_rate() which overwrites previous weight brackets.

        Args:
            service_rates_data: List of service rate dicts with service_id, zone_id, rate, etc.
            temp_to_real_id_map: Optional mapping of temp-{idx} IDs to real service IDs.
        """
        temp_to_real_id_map = temp_to_real_id_map or {}
        batch_updates = []

        for rate_data in service_rates_data:
            rate_dict = {k: v for k, v in rate_data.items() if v is not None}
            service_id = rate_dict.pop("service_id", None)
            zone_id = rate_dict.pop("zone_id", None)

            # Map temp service ID to real ID if needed
            if service_id and str(service_id).startswith("temp-"):
                service_id = temp_to_real_id_map.get(service_id, service_id)

            if service_id and zone_id:
                batch_updates.append({"service_id": service_id, "zone_id": zone_id, **rate_dict})

        if batch_updates:
            self.instance.batch_update_service_rates(batch_updates)

    def build_temp_to_real_service_map(self, services_data: list) -> dict:
        """Build mapping from temp-{idx} IDs to real service IDs.

        Uses service_name for matching new services (id=None) to handle
        duplicate service_codes (e.g. cloned services share the same code).
        Existing services (with id) are mapped directly by their known ID.
        """
        db_services = list(self.instance.services.all())
        name_to_ids = {}
        for s in db_services:
            name_to_ids.setdefault(s.service_name, []).append(s.id)

        used_ids = set()
        result = {}

        for idx, svc in enumerate(services_data):
            input_id = svc.get("id")

            if input_id:
                # Existing service — map temp-{idx} to its known ID
                result[f"temp-{idx}"] = input_id
                used_ids.add(input_id)
            else:
                # New service — find by name, avoiding already-used IDs
                name = svc.get("service_name")
                for candidate_id in name_to_ids.get(name, []):
                    if candidate_id not in used_ids:
                        result[f"temp-{idx}"] = candidate_id
                        used_ids.add(candidate_id)
                        break

        return result

    def update(self, instance, validated_data, **kwargs):
        """Handle updates of rate sheet data including services and carriers.

        When zones or surcharges data is provided, it's treated as a full replacement -
        zones/surcharges not in the incoming data will be removed.
        """
        services_data = validated_data.pop("services", None)
        carriers = validated_data.pop("carriers", None) if "carriers" in validated_data else None
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


@serializers.owned_model_serializer
class RateSheetModelSerializer(_RateSheetSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = providers.RateSheet
        exclude = ["created_at", "updated_at", "created_by"]
        extra_kwargs = {field: {"read_only": True} for field in ["id", "services"]}


class _SystemRateSheetSerializer(_RateSheetSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = providers.SystemRateSheet
        exclude = ["created_at", "updated_at", "created_by"]
        extra_kwargs = {field: {"read_only": True} for field in ["id", "services"]}

    context: dict = {}

    def __init__(self, *args, **kwargs):
        if "context" in kwargs:
            context = kwargs.pop("context")
            user = context.get("user") if isinstance(context, dict) else getattr(context, "user", None)
            self.context = {"user": user}
        super().__init__(*args, **kwargs)

    def create(self, validated_data):
        instance = super().create(validated_data)
        user = self.context.get("user") if isinstance(self.context, dict) else None
        if user:
            instance.created_by = user
            instance.save(update_fields=["created_by"])
        return instance


# Apply the same name for consistency
SystemRateSheetModelSerializer = _SystemRateSheetSerializer
