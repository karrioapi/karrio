import functools
import django.db.models as models
import django.core.validators as validators

import karrio.server.core.models as core
import karrio.server.core.datatypes as datatypes


@core.register_model
class ServiceLevel(core.OwnedEntity):
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

    zones = models.JSONField(blank=True, null=True, default=core.field_default([]))
    metadata = models.JSONField(blank=True, null=True, default=core.field_default({}))

    def __str__(self):
        return f"{self.id} | {self.service_name}"

    @property
    def object_type(self):
        return "service_level"
    
    @property 
    def computed_zones(self):
        """
        Computed property that returns zones in legacy format for backward compatibility.
        If the service belongs to a rate sheet with optimized structure, reconstruct from there.
        Otherwise, fall back to the service's own zones field.
        """
        # Check if this service belongs to a rate sheet with optimized structure
        rate_sheet = getattr(self, '_rate_sheet_cache', None)
        if not rate_sheet:
            # Try to find rate sheet this service belongs to
            try:
                rate_sheet = self.service_sheet.first()
                self._rate_sheet_cache = rate_sheet
            except:
                rate_sheet = None
        
        if rate_sheet and rate_sheet.zones and rate_sheet.service_rates:
            # Use optimized structure
            return rate_sheet.get_service_zones_legacy(self.id)
        else:
            # Fall back to legacy zones field
            return self.zones or []
    
    def update_zone_cell(self, zone_id: str, field: str, value):
        """Update a single field in a zone by ID or index with validation"""
        # Define allowed fields with their validators
        allowed_fields = {
            'rate': float,
            'min_weight': float,
            'max_weight': float,
            'transit_days': int,
            'transit_time': float,
            'label': str,
            'radius': float,
            'latitude': float,
            'longitude': float,
        }
        
        if field not in allowed_fields:
            raise ValueError(f"Field '{field}' is not allowed for zone updates")
        
        # Validate and convert the value
        try:
            if value is not None and value != '':
                value = allowed_fields[field](value)
        except (ValueError, TypeError):
            raise ValueError(f"Invalid value '{value}' for field '{field}' (expected {allowed_fields[field].__name__})")
        
        zones = self.zones or []
        
        # First try to find by zone ID
        for zone in zones:
            if zone.get('id') == zone_id:
                zone[field] = value
                self.save(update_fields=['zones'])
                return zone
        
        # Fallback: try to find by index for zones without IDs
        try:
            zone_index = int(zone_id)
            if 0 <= zone_index < len(zones):
                zones[zone_index][field] = value
                self.save(update_fields=['zones'])
                return zones[zone_index]
        except (ValueError, IndexError):
            pass
        
        raise ValueError(f"Zone {zone_id} not found")
    
    def batch_update_cells(self, updates: list):
        """
        Batch update multiple zone cells with validation
        updates format: [{'zone_id': str, 'field': str, 'value': any}, ...]
        """
        # Define allowed fields with their validators
        allowed_fields = {
            'rate': float,
            'min_weight': float,
            'max_weight': float,
            'transit_days': int,
            'transit_time': float,
            'label': str,
            'radius': float,
            'latitude': float,
            'longitude': float,
        }
        
        zones = list(self.zones or [])
        
        for update in updates:
            zone_id = update.get('zone_id')
            field = update.get('field')
            value = update.get('value')
            
            if field not in allowed_fields:
                raise ValueError(f"Field '{field}' is not allowed for zone updates")
            
            # Validate and convert the value
            try:
                if value is not None and value != '':
                    value = allowed_fields[field](value)
            except (ValueError, TypeError):
                raise ValueError(f"Invalid value '{value}' for field '{field}' (expected {allowed_fields[field].__name__})")
            
            # Find zone by ID first, then by index
            zone_found = False
            for zone in zones:
                if zone.get('id') == zone_id:
                    zone[field] = value
                    zone_found = True
                    break
            
            # Fallback to index if zone_id is numeric and zone not found by ID
            if not zone_found:
                try:
                    zone_index = int(zone_id)
                    if 0 <= zone_index < len(zones):
                        zones[zone_index][field] = value
                        zone_found = True
                except (ValueError, IndexError):
                    pass
            
            if not zone_found:
                raise ValueError(f"Zone {zone_id} not found")

        self.zones = zones
        self.save(update_fields=['zones'])
        return self.zones
