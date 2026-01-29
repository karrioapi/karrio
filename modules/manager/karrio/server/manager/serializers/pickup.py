import typing

from karrio.server import serializers
from karrio.server.serializers import (
    owned_model_serializer,
    save_one_to_one_data,
    Context,
    PlainDictField,
)
from karrio.server.core.gateway import Pickups, Connections
from karrio.server.core.datatypes import Confirmation
from karrio.server.core.utils import create_carrier_snapshot, resolve_carrier
from karrio.server.core.serializers import (
    Pickup,
    AddressData,
    PickupRequest,
    PickupUpdateRequest,
    PickupCancelRequest,
)
from karrio.server.manager.serializers import AddressSerializer
import karrio.server.manager.models as models

DEFAULT_CARRIER_FILTER: typing.Any = dict(active=True, capability="pickup")


def shipment_exists(value):
    validation = {
        key: models.Shipment.objects.filter(tracking_number=key) for key in value
    }

    if not all(val.exists() for val in validation.values()):
        invalids = [key for key, val in validation.items() if val.exists() is False]
        raise serializers.ValidationError(
            f"Shipment with the tracking numbers: {invalids} not found", code="invalid"
        )

    if any(val.first().shipment_pickup.exists() for val in validation.values()):
        scheduled = [
            key
            for key, val in validation.items()
            if val.first().shipment_pickup.exists() is True
        ]
        raise serializers.ValidationError(
            f"The following shipments {scheduled} are already scheduled for pickups",
            code="invalid",
        )


def pickup_exists(value):
    validation = {
        key: models.Pickup.objects.filter(tracking_number=key).exists() for key in value
    }

    if not all(validation.values()):
        invalids = [key for key, val in validation.items() if val is False]
        raise serializers.ValidationError(
            f"Shipment with the tracking numbers: {invalids} not found", code="invalid"
        )


def address_exists(value):
    if value is str and not models.Address.objects.filter(pk=value).exists():
        raise serializers.ValidationError(
            {"address": f"Address with id {value} not found: {value}"}, code="invalid"
        )


class PickupSerializer(PickupRequest):
    parcels = None
    address = AddressData(
        required=False, validators=[address_exists], help_text="The pickup address"
    )
    tracking_numbers = serializers.StringListField(
        required=False,
        validators=[shipment_exists],
        help_text="The list of shipments to be picked up (optional if parcels_count provided)",
    )
    parcels_count = serializers.IntegerField(
        required=False,
        allow_null=True,
        min_value=1,
        help_text="The number of parcels to be picked up (alternative to linking shipments)",
    )
    metadata = PlainDictField(
        required=False, default={}, help_text="User metadata for the pickup"
    )

    def __init__(self, instance: models.Pickup = None, **kwargs):
        self._shipments: typing.List[models.Shipment] = []

        if "data" in kwargs:
            data = kwargs.get("data").copy()
            tracking_numbers = data.get("tracking_numbers", [])

            # Only fetch shipments if tracking_numbers provided
            if tracking_numbers:
                self._shipments = list(
                    models.Shipment.objects.filter(
                        tracking_number__in=tracking_numbers
                    )
                )

            # Address resolution logic
            if data.get("address") is None and instance is None:
                # Try to get address from linked shipments
                address = next(
                    (s.shipper for s in self._shipments if s.shipper), None
                )
            elif data.get("address") is None and instance is not None:
                # Use existing instance address
                address = instance.address
            elif isinstance(data.get("address"), str):
                # Legacy: look up address by ID
                address = models.Address.objects.get(pk=data.get("address"))
            else:
                address = data.get("address")

            if address is not None:
                data.update(address=address)

            kwargs.update(data=data)

        super().__init__(instance, **kwargs)

    def validate(self, data):
        validated_data = super(PickupRequest, self).validate(data)

        tracking_numbers = validated_data.get("tracking_numbers", [])
        parcels_count = validated_data.get("parcels_count")
        address = validated_data.get("address")

        # Must have at least one source of parcel info
        if not tracking_numbers and not parcels_count:
            raise serializers.ValidationError(
                "At least one of tracking_numbers or parcels_count must be provided",
                code="required"
            )

        # Address required for standalone pickups (no tracking_numbers)
        if not tracking_numbers and not address:
            raise serializers.ValidationError(
                "address is required when not linking to shipments",
                code="required"
            )

        # Existing validation for multi-shipment pickups
        if len(tracking_numbers) > 1 and address is None:
            raise serializers.ValidationError(
                "address must be specified for multi-shipments pickup",
                code="required"
            )

        return validated_data


@owned_model_serializer
class PickupData(PickupSerializer):
    def create(self, validated_data: dict, context: Context, **kwargs) -> models.Pickup:
        carrier_filter = validated_data["carrier_filter"]
        parcels_count = validated_data.get("parcels_count")
        pickup_type = validated_data.get("pickup_type", "one_time")
        recurrence = validated_data.get("recurrence") or {}

        # Extract shipment identifiers only if shipments linked
        shipment_identifiers = []
        billing_number = None

        if self._shipments:
            shipment_identifiers = [
                _
                for shipment in self._shipments
                for _ in set(
                    [
                        *(shipment.meta.get("shipment_identifiers") or []),
                        shipment.shipment_identifier,
                    ]
                )
            ]
            # Extract billing_number from first shipment's meta (if available)
            billing_number = next(
                (s.meta.get("billing_number") for s in self._shipments if s.meta.get("billing_number")),
                None,
            )

        carrier = Connections.first(
            context=context,
            **{"raise_not_found": True, **DEFAULT_CARRIER_FILTER, **carrier_filter},
        )

        # Determine parcels source
        if self._shipments:
            # Mode 1: Parcels from linked shipments
            parcels_list = sum([(s.parcels or []) for s in self._shipments], [])
        elif parcels_count:
            # Mode 2: Generate placeholder parcels from count
            parcels_list = [{"id": f"parcel_{i+1}"} for i in range(parcels_count)]
        else:
            parcels_list = []

        # Build request data directly (address is now a JSON dict)
        # Exclude non-serializable fields from request data
        excluded_keys = {"created_by", "carrier_filter", "tracking_numbers", "parcels_count", "recurrence"}
        filtered_data = {k: v for k, v in validated_data.items() if k not in excluded_keys}

        request_data = {
            **filtered_data,
            "parcels": parcels_list,
            "options": {
                **({"shipment_identifiers": shipment_identifiers} if shipment_identifiers else {}),
                **({"billing_number": billing_number} if billing_number else {}),
                **(validated_data.get("options") or {}),
            },
        }

        response = Pickups.schedule(payload=request_data, carrier=carrier)
        payload = {
            key: value
            for key, value in Pickup(response.pickup).data.items()
            if key in models.Pickup.DIRECT_PROPS
        }

        # Use the address from validated_data directly (JSON field)
        address_data = validated_data.get("address") or {}

        # Build meta with pickup_type and recurrence (stored in meta per PRD)
        meta_data = {
            **(payload.get("meta") or {}),
            "pickup_type": pickup_type,
            **({"recurrence": recurrence} if recurrence else {}),
        }

        pickup = models.Pickup.objects.create(
            **{
                **payload,
                "address": address_data,
                "carrier": create_carrier_snapshot(carrier),
                "created_by": context.user,
                "test_mode": response.pickup.test_mode,
                "confirmation_number": response.pickup.confirmation_number,
                "meta": meta_data,
            }
        )
        pickup.shipments.set(self._shipments)

        return pickup


@owned_model_serializer
class PickupUpdateData(PickupSerializer):
    confirmation_number = serializers.CharField(
        required=True, help_text="pickup identification number"
    )
    pickup_date = serializers.CharField(
        required=False,
        help_text="""The expected pickup date.<br/>
        Date Format: YYYY-MM-DD
        """,
    )
    ready_time = serializers.CharField(
        required=False,
        allow_blank=True,
        allow_null=True,
        help_text="The ready time for pickup.",
    )
    closing_time = serializers.CharField(
        required=False,
        allow_blank=True,
        allow_null=True,
        help_text="The closing or late time of the pickup",
    )
    instruction = serializers.CharField(
        required=False,
        allow_blank=True,
        allow_null=True,
        help_text="""The pickup instruction.<br/>
        eg: Handle with care.
        """,
    )
    package_location = serializers.CharField(
        required=False,
        allow_blank=True,
        allow_null=True,
        help_text="""The package(s) location.<br/>
        eg: Behind the entrance door.
        """,
    )
    tracking_numbers = serializers.StringListField(
        required=False,
        validators=[shipment_exists],
        help_text="The list of shipments to be picked up",
    )

    def validate(self, data):
        """Override validation for update - existing pickups don't need parcel source validation."""
        # Skip the parent's tracking_numbers/parcels_count validation for updates
        # The pickup already exists with its parcels, we're just updating details
        validated_data = serializers.Serializer.validate(self, data)

        # Only validate multi-shipment address requirement if tracking_numbers provided
        tracking_numbers = validated_data.get("tracking_numbers", [])
        if len(tracking_numbers) > 1 and validated_data.get("address") is None:
            raise serializers.ValidationError(
                "address must be specified for multi-shipments pickup",
                code="required"
            )

        return validated_data

    def update(
        self, instance: models.Pickup, validated_data: dict, context: dict, **kwargs
    ) -> models.Tracking:
        shipment_identifiers = [
            _
            for shipment in self._shipments
            for _ in set(
                [
                    *(shipment.meta.get("shipment_identifiers") or []),
                    shipment.shipment_identifier,
                ]
            )
        ]

        # Merge existing address with updates (address is now a JSON field)
        existing_address = instance.address or {}
        address_updates = validated_data.get("address") or {}
        merged_address = {**existing_address, **address_updates}

        # Extract pickup_type and recurrence for meta
        pickup_type = validated_data.get("pickup_type") or (instance.meta or {}).get("pickup_type", "one_time")
        recurrence = validated_data.get("recurrence") or (instance.meta or {}).get("recurrence")

        # Build base data from instance fields directly (not via serializer)
        # Convert date to string for serializer validation
        pickup_date = (
            str(instance.pickup_date) if instance.pickup_date else None
        )
        base_data = {
            "pickup_date": pickup_date,
            "address": existing_address,
            "parcels": instance.parcels,
            "confirmation_number": instance.confirmation_number,
            "ready_time": instance.ready_time,
            "closing_time": instance.closing_time,
            "instruction": instance.instruction,
            "package_location": instance.package_location,
            "options": instance.options or {},
            "pickup_type": pickup_type,
        }

        # Extract billing_number from first shipment's meta (if available)
        billing_number = next(
            (s.meta.get("billing_number") for s in self._shipments if s.meta.get("billing_number")),
            None,
        )

        # Build request data directly (data comes from trusted sources)
        request_data = {
            **base_data,
            **validated_data,
            "address": merged_address,
            "options": {
                "shipment_identifiers": shipment_identifiers,
                **({"billing_number": billing_number} if billing_number else {}),
                **(instance.meta or {}),
                **(validated_data.get("options") or {}),
            },
        }

        # Resolve carrier from snapshot for API call
        carrier = resolve_carrier(instance.carrier, context)
        Pickups.update(payload=request_data, carrier=carrier)

        data = validated_data.copy()
        for key, val in data.items():
            # Skip address and meta-stored fields - they need special handling
            if key in ("address", "pickup_type", "recurrence"):
                continue
            if key in models.Pickup.DIRECT_PROPS:
                setattr(instance, key, val)

        # Always set the merged address (preserves existing fields while applying updates)
        instance.address = merged_address

        # Update meta with pickup_type and recurrence
        existing_meta = instance.meta or {}
        instance.meta = {
            **existing_meta,
            "pickup_type": pickup_type,
            **({"recurrence": recurrence} if recurrence else {}),
        }

        instance.save()
        return instance


class PickupCancelData(serializers.Serializer):
    reason = serializers.CharField(
        required=False, help_text="The reason of the pickup cancellation"
    )

    def update(
        self, instance: models.Pickup, validated_data: dict, context: Context = None, **kwargs
    ) -> Confirmation:
        request = PickupCancelRequest(
            {**PickupCancelRequest(instance).data, **validated_data}
        )
        # Resolve carrier from snapshot for API call
        carrier = resolve_carrier(instance.carrier, context)
        Pickups.cancel(payload=request.data, carrier=carrier)
        instance.delete()

        return instance
