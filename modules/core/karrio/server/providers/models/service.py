import functools
import django.db.models as models
import django.core.validators as validators

import karrio.server.core.models as core
import karrio.server.core.datatypes as datatypes


@core.register_model
class ServiceLevel(core.OwnedEntity):
    """
    Service level definition for rate sheet-based shipping.

    Services reference shared zones and surcharges defined at the RateSheet level
    via zone_ids and surcharge_ids. Rate values are stored in RateSheet.service_rates.
    """

    class Meta:
        db_table = "service-level"
        verbose_name = "Service Level"
        verbose_name_plural = "Service Levels"
        ordering = ["-created_at"]

    id = models.CharField(
        max_length=50,
        primary_key=True,
        default=functools.partial(core.uuid, prefix="svc_"),
        editable=False,
    )
    service_name = models.CharField(max_length=50)
    service_code = models.CharField(
        max_length=50, validators=[validators.RegexValidator(r"^[a-z0-9_]+$")]
    )
    carrier_service_code = models.CharField(max_length=50, null=True, blank=True)
    description = models.CharField(max_length=250, null=True, blank=True)
    active = models.BooleanField(null=True, default=True)

    currency = models.CharField(
        max_length=4, choices=datatypes.CURRENCIES, null=True, blank=True
    )

    transit_days = models.IntegerField(blank=True, null=True)
    transit_time = models.FloatField(blank=True, null=True)

    max_width = models.FloatField(blank=True, null=True)
    max_height = models.FloatField(blank=True, null=True)
    max_length = models.FloatField(blank=True, null=True)
    dimension_unit = models.CharField(
        max_length=2, choices=datatypes.DIMENSION_UNITS, null=True, blank=True
    )

    min_weight = models.FloatField(blank=True, null=True)
    max_weight = models.FloatField(blank=True, null=True)
    weight_unit = models.CharField(
        max_length=2, choices=datatypes.WEIGHT_UNITS, null=True, blank=True
    )

    domicile = models.BooleanField(null=True)
    international = models.BooleanField(null=True)

    # ─────────────────────────────────────────────────────────────────
    # VOLUMETRIC WEIGHT
    # ─────────────────────────────────────────────────────────────────
    max_volume = models.FloatField(
        blank=True,
        null=True,
        help_text="Maximum volume in liters for volumetric weight calculation",
    )
    dim_factor = models.FloatField(
        blank=True,
        null=True,
        help_text="Dimensional weight divisor. 5000-6000 for cm/kg, 139-166 for in/lb",
    )
    use_volumetric = models.BooleanField(
        default=False,
        help_text="Use max(actual_weight, volumetric_weight) for rate calculation",
    )

    # ─────────────────────────────────────────────────────────────────
    # COST TRACKING (internal - not shown to customer)
    # ─────────────────────────────────────────────────────────────────
    cost = models.FloatField(
        blank=True,
        null=True,
        help_text="Base COGS (Cost of Goods Sold) - internal cost tracking",
    )

    # ─────────────────────────────────────────────────────────────────
    # ZONE & SURCHARGE REFERENCES
    # These reference shared definitions at the RateSheet level
    # ─────────────────────────────────────────────────────────────────
    zone_ids = models.JSONField(
        blank=True,
        null=True,
        default=core.field_default([]),
        help_text="List of zone IDs this service applies to: ['zone_1', 'zone_2']",
    )
    surcharge_ids = models.JSONField(
        blank=True,
        null=True,
        default=core.field_default([]),
        help_text="List of surcharge IDs to apply: ['surch_fuel', 'surch_residential']",
    )

    metadata = models.JSONField(blank=True, null=True, default=core.field_default({}))

    # ─────────────────────────────────────────────────────────────────
    # SERVICE FEATURES
    # ─────────────────────────────────────────────────────────────────
    features = models.JSONField(
        blank=True,
        null=True,
        default=core.field_default({}),
        help_text="Structured features: {first_mile, last_mile, form_factor, b2c, b2b, tracked, ...}",
    )

    def __str__(self):
        return f"{self.id} | {self.service_name}"

    @property
    def object_type(self):
        return "service_level"

    @property
    def rate_sheet(self):
        """Get the rate sheet this service belongs to."""
        return self.service_sheet.first()

    @property
    def zones(self):
        """
        Get zones as ServiceZone objects for SDK compatibility.

        Transforms zone_ids + rate_sheet data into the ServiceZone format
        expected by the RatingMixinProxy. Each service_rate entry becomes
        a separate ServiceZone (supporting multiple weight brackets per zone).
        """
        _rate_sheet = self.rate_sheet
        if not _rate_sheet:
            return []

        zones_by_id = {z.get("id"): z for z in (_rate_sheet.zones or [])}

        # Get all service_rates for this service (may have multiple per zone_id for weight brackets)
        service_rates = [
            sr for sr in (_rate_sheet.service_rates or [])
            if sr.get("service_id") == self.id
            and sr.get("zone_id") in (self.zone_ids or [])
        ]

        result = []
        for rate_data in service_rates:
            zone_id = rate_data.get("zone_id")
            zone_def = zones_by_id.get(zone_id)

            if not zone_def:
                continue

            # Build ServiceZone-compatible dict (one per service_rate entry)
            result.append({
                "id": zone_id,
                "label": zone_def.get("label"),
                "rate": rate_data.get("rate"),
                "cost": rate_data.get("cost"),
                "min_weight": rate_data.get("min_weight"),
                "max_weight": rate_data.get("max_weight"),
                "transit_days": rate_data.get("transit_days") or zone_def.get("transit_days"),
                "transit_time": rate_data.get("transit_time") or zone_def.get("transit_time"),
                "country_codes": zone_def.get("country_codes") or [],
                "postal_codes": zone_def.get("postal_codes") or [],
                "cities": zone_def.get("cities") or [],
                "radius": zone_def.get("radius"),
                "latitude": zone_def.get("latitude"),
                "longitude": zone_def.get("longitude"),
            })

        return result

    @property
    def surcharges(self):
        """
        Get surcharges as Surcharge objects for SDK compatibility.

        Transforms surcharge_ids + rate_sheet data into the Surcharge format
        expected by the RatingMixinProxy.
        """
        _rate_sheet = self.rate_sheet
        if not _rate_sheet:
            return []

        surcharges_by_id = {s.get("id"): s for s in (_rate_sheet.surcharges or [])}

        result = []
        for surcharge_id in (self.surcharge_ids or []):
            surcharge_def = surcharges_by_id.get(surcharge_id)
            if not surcharge_def or not surcharge_def.get("active", True):
                continue

            result.append({
                "id": surcharge_id,
                "name": surcharge_def.get("name"),
                "amount": surcharge_def.get("amount"),
                "surcharge_type": surcharge_def.get("surcharge_type", "fixed"),
                "cost": surcharge_def.get("cost"),
                "active": surcharge_def.get("active", True),
            })

        return result

    def get_rate_for_zone(self, zone_id: str) -> dict:
        """
        Get the rate for a specific zone from the parent rate sheet.

        Returns:
            dict: Rate data including rate, cost, min_weight, max_weight, transit_days
        """
        rate_sheet = self.rate_sheet
        if not rate_sheet:
            return None
        return rate_sheet.get_service_rate(self.id, zone_id)

    def get_applicable_surcharges(self) -> list:
        """
        Get the applicable surcharges from the parent rate sheet.

        Returns:
            list: List of surcharge definitions
        """
        rate_sheet = self.rate_sheet
        if not rate_sheet:
            return []

        surcharges = []
        for surcharge_id in (self.surcharge_ids or []):
            surcharge = rate_sheet.get_surcharge(surcharge_id)
            if surcharge and surcharge.get('active', True):
                surcharges.append(surcharge)
        return surcharges

    def calculate_rate(self, zone_id: str) -> tuple:
        """
        Calculate the total rate for a zone including surcharges.

        Args:
            zone_id: The zone ID to calculate rate for

        Returns:
            tuple: (total_rate, breakdown) where breakdown includes base rate and surcharges
        """
        rate_sheet = self.rate_sheet
        if not rate_sheet:
            return 0, []

        # Get base rate for zone
        rate_data = rate_sheet.get_service_rate(self.id, zone_id)
        base_rate = float(rate_data.get('rate', 0)) if rate_data else 0

        # Apply surcharges
        total_rate, surcharge_breakdown = rate_sheet.apply_surcharges_to_rate(
            base_rate, self.surcharge_ids or []
        )

        return total_rate, {
            'base_rate': base_rate,
            'base_cost': rate_data.get('cost') if rate_data else None,
            'surcharges': surcharge_breakdown,
            'total': total_rate,
        }
