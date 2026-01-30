import functools
import django.db.models as models
import django.utils.translation as translation

import django.conf as conf
import karrio.server.core.models as core

_ = translation.gettext_lazy


@core.register_model
class RateSheet(core.OwnedEntity):
    """
    Rate sheet with shared zones, surcharges, and service-zone rate mappings.

    Structure:
    - zones: Shared geographic zone definitions
    - surcharges: Shared surcharge definitions (fuel, handling, etc.)
    - service_rates: Service-zone rate mappings with weights and transit times
    - services: Service level definitions that reference zones/surcharges by ID
    """

    class Meta:
        db_table = "rate-sheet"
        verbose_name = "Rate Sheet"
        verbose_name_plural = "Rate Sheets"
        ordering = ["-created_at"]

    id = models.CharField(
        max_length=50,
        editable=False,
        primary_key=True,
        default=functools.partial(core.uuid, prefix="rsht_"),
    )
    name = models.CharField(_("name"), max_length=50, db_index=True)
    slug = models.CharField(_("slug"), max_length=50, db_index=True)
    carrier_name = models.CharField(max_length=50, db_index=True)
    is_system = models.BooleanField(default=False, db_index=True)
    origin_countries = models.JSONField(
        blank=True,
        null=True,
        default=core.field_default([]),
        help_text="List of origin country codes this rate sheet applies to",
    )
    services = models.ManyToManyField(
        "ServiceLevel", blank=True, related_name="service_sheet"
    )

    # ─────────────────────────────────────────────────────────────────
    # SHARED ZONE DEFINITIONS
    # Structure: [{'id': 'zone_1', 'label': 'Zone 1', 'country_codes': [...], 'cities': [...], 'postal_codes': [...], 'transit_days': int}]
    # ─────────────────────────────────────────────────────────────────
    zones = models.JSONField(
        blank=True,
        null=True,
        default=core.field_default([]),
        help_text="Shared zone definitions: [{'id': 'zone_1', 'label': 'Zone 1', 'cities': [...], 'country_codes': [...]}]",
    )

    # ─────────────────────────────────────────────────────────────────
    # SHARED SURCHARGE DEFINITIONS
    # Structure: [{'id': 'surch_1', 'name': 'Fuel', 'amount': 8.5, 'surcharge_type': 'percentage', 'cost': 5.2, 'active': true}]
    # ─────────────────────────────────────────────────────────────────
    surcharges = models.JSONField(
        blank=True,
        null=True,
        default=core.field_default([]),
        help_text="Shared surcharge definitions: [{'id': 'surch_1', 'name': 'Fuel', 'amount': 8.5, 'surcharge_type': 'percentage'}]",
    )

    # ─────────────────────────────────────────────────────────────────
    # SERVICE-ZONE RATE MAPPING
    # Structure: [{'service_id': 'svc_1', 'zone_id': 'zone_1', 'rate': 10.50, 'cost': 8.00, 'min_weight': 0, 'max_weight': 5}]
    # ─────────────────────────────────────────────────────────────────
    service_rates = models.JSONField(
        blank=True,
        null=True,
        default=core.field_default([]),
        help_text="Service-zone rate mapping: [{'service_id': 'svc_1', 'zone_id': 'zone_1', 'rate': 10.50}]",
    )

    metadata = models.JSONField(
        blank=True,
        null=True,
        default=core.field_default({}),
    )

    created_by = models.ForeignKey(
        conf.settings.AUTH_USER_MODEL,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        editable=False,
    )

    def delete(self, *args, **kwargs):
        self.services.all().delete()
        return super().delete(*args, **kwargs)

    @property
    def object_type(self):
        return "rate-sheet"

    @property
    def carriers(self):
        import karrio.server.providers.models as providers

        return providers.CarrierConnection.objects.filter(
            carrier_code=self.carrier_name, rate_sheet__id=self.id
        )

    # ─────────────────────────────────────────────────────────────────
    # ZONE MANAGEMENT
    # ─────────────────────────────────────────────────────────────────

    def add_zone(self, zone_data: dict) -> str:
        """Add a new shared zone definition."""
        zones = list(self.zones or [])

        # Generate zone ID if not provided
        if not zone_data.get("id"):
            zone_data["id"] = f"zone_{len(zones) + 1}"

        zones.append(zone_data)
        self.zones = zones
        self.save(update_fields=["zones"])
        return zone_data["id"]

    def update_zone(self, zone_id: str, zone_data: dict) -> dict:
        """Update a shared zone definition."""
        zones = list(self.zones or [])

        for i, zone in enumerate(zones):
            if zone.get("id") == zone_id:
                zones[i] = {"id": zone_id, **{k: v for k, v in zone_data.items() if k != "id"}}
                self.zones = zones
                self.save(update_fields=["zones"])
                return zones[i]

        raise ValueError(f"Zone {zone_id} not found")

    def remove_zone(self, zone_id: str):
        """Remove a zone and all its associated rates."""
        zones = [z for z in (self.zones or []) if z.get("id") != zone_id]
        self.zones = zones

        # Remove all rates for this zone
        service_rates = [sr for sr in (self.service_rates or []) if sr.get("zone_id") != zone_id]
        self.service_rates = service_rates

        # Remove zone_id from services
        for service in self.services.all():
            if zone_id in (service.zone_ids or []):
                service.zone_ids = [zid for zid in service.zone_ids if zid != zone_id]
                service.save(update_fields=["zone_ids"])

        self.save(update_fields=["zones", "service_rates"])

    def get_zone(self, zone_id: str) -> dict:
        """Get a zone by ID."""
        for zone in self.zones or []:
            if zone.get("id") == zone_id:
                return zone
        return None

    # ─────────────────────────────────────────────────────────────────
    # SURCHARGE MANAGEMENT
    # ─────────────────────────────────────────────────────────────────

    def add_surcharge(self, surcharge_data: dict) -> str:
        """Add a new shared surcharge definition."""
        surcharges = list(self.surcharges or [])

        if not surcharge_data.get("id"):
            surcharge_data["id"] = f"surch_{len(surcharges) + 1}"

        surcharge_data.setdefault("active", True)
        surcharge_data.setdefault("surcharge_type", "fixed")

        surcharges.append(surcharge_data)
        self.surcharges = surcharges
        self.save(update_fields=["surcharges"])
        return surcharge_data["id"]

    def update_surcharge(self, surcharge_id: str, surcharge_data: dict) -> dict:
        """Update a shared surcharge definition."""
        surcharges = list(self.surcharges or [])

        for i, surcharge in enumerate(surcharges):
            if surcharge.get("id") == surcharge_id:
                surcharges[i] = {"id": surcharge_id, **{k: v for k, v in surcharge_data.items() if k != "id"}}
                self.surcharges = surcharges
                self.save(update_fields=["surcharges"])
                return surcharges[i]

        raise ValueError(f"Surcharge {surcharge_id} not found")

    def remove_surcharge(self, surcharge_id: str):
        """Remove a surcharge definition and its references from services."""
        surcharges = [s for s in (self.surcharges or []) if s.get("id") != surcharge_id]
        self.surcharges = surcharges

        # Remove surcharge_id from services
        for service in self.services.all():
            if surcharge_id in (service.surcharge_ids or []):
                service.surcharge_ids = [sid for sid in service.surcharge_ids if sid != surcharge_id]
                service.save(update_fields=["surcharge_ids"])

        self.save(update_fields=["surcharges"])

    def batch_update_surcharges(self, updates: list):
        """Batch update multiple surcharges."""
        surcharges = list(self.surcharges or [])
        surcharge_map = {s.get("id"): i for i, s in enumerate(surcharges)}

        for update in updates:
            surcharge_id = update.get("id")
            if not surcharge_id:
                continue

            if surcharge_id in surcharge_map:
                idx = surcharge_map[surcharge_id]
                surcharges[idx] = {**surcharges[idx], **update}
            else:
                update.setdefault("active", True)
                update.setdefault("surcharge_type", "fixed")
                surcharges.append(update)
                surcharge_map[surcharge_id] = len(surcharges) - 1

        self.surcharges = surcharges
        self.save(update_fields=["surcharges"])

    def get_surcharge(self, surcharge_id: str) -> dict:
        """Get a surcharge by ID."""
        for surcharge in self.surcharges or []:
            if surcharge.get("id") == surcharge_id:
                return surcharge
        return None

    # ─────────────────────────────────────────────────────────────────
    # SERVICE RATE MANAGEMENT
    # ─────────────────────────────────────────────────────────────────

    def _make_rate_key(self, rate: dict) -> str:
        """Generate a unique key for a rate entry including weight brackets."""
        service_id = rate.get("service_id", "")
        zone_id = rate.get("zone_id", "")
        min_weight = rate.get("min_weight", 0)
        max_weight = rate.get("max_weight", 0)
        return f"{service_id}:{zone_id}:{min_weight}:{max_weight}"

    def get_service_rate(self, service_id: str, zone_id: str, min_weight: float = None, max_weight: float = None) -> dict:
        """Get a service rate by service_id, zone_id, and optionally weight range."""
        for rate in self.service_rates or []:
            if rate.get("service_id") == service_id and rate.get("zone_id") == zone_id:
                if min_weight is not None and max_weight is not None:
                    if rate.get("min_weight") == min_weight and rate.get("max_weight") == max_weight:
                        return rate
                else:
                    return rate
        return None

    def get_service_rates(self, service_id: str, zone_id: str) -> list:
        """Get all service rates for a service_id and zone_id combination."""
        return [
            rate for rate in self.service_rates or []
            if rate.get("service_id") == service_id and rate.get("zone_id") == zone_id
        ]

    def update_service_rate(self, service_id: str, zone_id: str, rate_data: dict) -> dict:
        """Update or create a service-zone rate mapping.
        Uses (service_id, zone_id, min_weight, max_weight) as the unique key.
        Falls back to (service_id, zone_id) match when no exact key match exists."""
        service_rates = list(self.service_rates or [])
        min_weight = rate_data.get("min_weight", 0)
        max_weight = rate_data.get("max_weight", 0)
        target_key = f"{service_id}:{zone_id}:{min_weight}:{max_weight}"

        # First try exact composite key match
        for i, rate in enumerate(service_rates):
            rate_key = self._make_rate_key(rate)
            if rate_key == target_key:
                service_rates[i] = {"service_id": service_id, "zone_id": zone_id, **rate_data}
                self.service_rates = service_rates
                self.save(update_fields=["service_rates"])
                return service_rates[i]

        # Fallback: match by (service_id, zone_id) if a single entry exists
        matches = [
            (i, r) for i, r in enumerate(service_rates)
            if r.get("service_id") == service_id and r.get("zone_id") == zone_id
        ]
        if len(matches) == 1:
            idx = matches[0][0]
            service_rates[idx] = {"service_id": service_id, "zone_id": zone_id, **rate_data}
            self.service_rates = service_rates
            self.save(update_fields=["service_rates"])
            return service_rates[idx]

        # Create new rate record
        new_rate = {"service_id": service_id, "zone_id": zone_id, **rate_data}
        service_rates.append(new_rate)
        self.service_rates = service_rates
        self.save(update_fields=["service_rates"])
        return new_rate

    def batch_update_service_rates(self, updates: list):
        """
        Batch update service rates.
        Uses (service_id, zone_id, min_weight, max_weight) as the unique key.
        updates format: [{'service_id': str, 'zone_id': str, 'rate': float, 'cost': float,
                          'min_weight': float, 'max_weight': float, ...}, ...]
        """
        service_rates = list(self.service_rates or [])
        rate_map = {}

        for i, rate in enumerate(service_rates):
            key = self._make_rate_key(rate)
            rate_map[key] = i

        for update in updates:
            service_id = update.get("service_id")
            zone_id = update.get("zone_id")
            if not service_id or not zone_id:
                continue

            key = self._make_rate_key(update)

            if key in rate_map:
                service_rates[rate_map[key]] = {**service_rates[rate_map[key]], **update}
            else:
                service_rates.append(update)
                rate_map[key] = len(service_rates) - 1

        self.service_rates = service_rates
        self.save(update_fields=["service_rates"])

    def remove_service_rate(self, service_id: str, zone_id: str, min_weight: float = None, max_weight: float = None):
        """Remove a service-zone rate mapping.
        If min_weight and max_weight are provided, removes only the specific weight bracket.
        Otherwise, removes all rates for the service+zone combination."""
        if min_weight is not None and max_weight is not None:
            target_key = f"{service_id}:{zone_id}:{min_weight}:{max_weight}"
            service_rates = [
                sr for sr in (self.service_rates or [])
                if self._make_rate_key(sr) != target_key
            ]
        else:
            service_rates = [
                sr
                for sr in (self.service_rates or [])
                if not (sr.get("service_id") == service_id and sr.get("zone_id") == zone_id)
            ]
        self.service_rates = service_rates
        self.save(update_fields=["service_rates"])

    # ─────────────────────────────────────────────────────────────────
    # RATE CALCULATION
    # ─────────────────────────────────────────────────────────────────

    def apply_surcharges_to_rate(self, base_rate: float, surcharge_ids: list) -> tuple:
        """
        Apply surcharges to a base rate.

        Args:
            base_rate: The base rate before surcharges
            surcharge_ids: List of surcharge IDs to apply

        Returns:
            tuple: (final_rate, breakdown)
        """
        total_surcharge = 0.0
        breakdown = []

        for surcharge_id in surcharge_ids:
            surcharge = self.get_surcharge(surcharge_id)
            if not surcharge or not surcharge.get("active", True):
                continue

            name = surcharge.get("name", "Surcharge")
            amount = float(surcharge.get("amount", 0))
            surcharge_type = surcharge.get("surcharge_type", "fixed")

            applied_amount = (base_rate * amount / 100) if surcharge_type == "percentage" else amount
            total_surcharge += applied_amount
            breakdown.append(
                {
                    "id": surcharge_id,
                    "name": name,
                    "amount": applied_amount,
                    "surcharge_type": surcharge_type,
                    "original_value": amount,
                    "cost": surcharge.get("cost"),
                }
            )

        return base_rate + total_surcharge, breakdown

    def calculate_rate(self, service_id: str, zone_id: str) -> tuple:
        """
        Calculate the total rate for a service-zone combination including surcharges.

        Returns:
            tuple: (total_rate, breakdown)
        """
        rate_data = self.get_service_rate(service_id, zone_id)
        base_rate = float(rate_data.get("rate", 0)) if rate_data else 0

        # Get service surcharge_ids
        service = self.services.filter(id=service_id).first()
        surcharge_ids = service.surcharge_ids if service else []

        total_rate, surcharge_breakdown = self.apply_surcharges_to_rate(base_rate, surcharge_ids or [])

        return total_rate, {
            "base_rate": base_rate,
            "base_cost": rate_data.get("cost") if rate_data else None,
            "surcharges": surcharge_breakdown,
            "total": total_rate,
        }

    def get_service_zones_for_rating(self, service_id: str) -> list:
        """
        Get zones with rates for a service, formatted for SDK rate calculation.

        Returns:
            list: Zone dicts with rate data merged from service_rates
        """
        zones = self.zones or []
        service_rates = self.service_rates or []

        # Build rate lookup
        rate_map = {
            sr.get("zone_id"): sr
            for sr in service_rates
            if sr.get("service_id") == service_id
        }

        # Merge zone definitions with rates
        result = []
        for zone in zones:
            zone_id = zone.get("id")
            rate_data = rate_map.get(zone_id, {})

            result.append({
                "id": zone_id,
                "label": zone.get("label"),
                "rate": rate_data.get("rate", 0),
                "cost": rate_data.get("cost"),
                "min_weight": rate_data.get("min_weight"),
                "max_weight": rate_data.get("max_weight"),
                "transit_days": rate_data.get("transit_days") or zone.get("transit_days"),
                "transit_time": rate_data.get("transit_time") or zone.get("transit_time"),
                "radius": zone.get("radius"),
                "latitude": zone.get("latitude"),
                "longitude": zone.get("longitude"),
                "cities": zone.get("cities", []),
                "postal_codes": zone.get("postal_codes", []),
                "country_codes": zone.get("country_codes", []),
            })

        return result

    def get_surcharges_for_rating(self, surcharge_ids: list) -> list:
        """
        Get surcharges formatted for SDK rate calculation.

        Args:
            surcharge_ids: List of surcharge IDs to include

        Returns:
            list: Surcharge dicts for active surcharges
        """
        result = []
        for surcharge_id in surcharge_ids or []:
            surcharge = self.get_surcharge(surcharge_id)
            if surcharge and surcharge.get("active", True):
                result.append({
                    "id": surcharge.get("id"),
                    "name": surcharge.get("name"),
                    "amount": surcharge.get("amount", 0),
                    "surcharge_type": surcharge.get("surcharge_type", "fixed"),
                    "cost": surcharge.get("cost"),
                    "active": surcharge.get("active", True),
                })
        return result