import functools
import django.db.models as models
import django.utils.translation as translation

import django.conf as conf
import karrio.server.core.models as core

_ = translation.gettext_lazy


@core.register_model
class RateSheet(core.OwnedEntity):
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
    services = models.ManyToManyField(
        "ServiceLevel", blank=True, related_name="service_sheet"
    )
    
    # New optimized structure
    zones = models.JSONField(
        blank=True,
        null=True,
        default=core.field_default([]),
        help_text="Shared zone definitions: [{'id': 'zone_1', 'label': 'Zone 1', 'cities': [...], 'country_codes': [...]}]"
    )
    service_rates = models.JSONField(
        blank=True,
        null=True,
        default=core.field_default([]),
        help_text="Service-zone rate mapping: [{'service_id': 'svc_1', 'zone_id': 'zone_1', 'rate': 10.50}]"
    )
    
    # Keep old structure for backward compatibility during migration
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

        return providers.Carrier.objects.filter(
            carrier_code=self.carrier_name, rate_sheet__id=self.id
        )
    
    def get_service_zones_legacy(self, service_id: str):
        """
        Backward compatible method - returns zones in old format for SDK compatibility
        Combines shared zones with service-specific rates
        """
        zones = self.zones or []
        service_rates = self.service_rates or []
        
        # Get rates for this service
        service_rate_map = {
            sr['zone_id']: sr for sr in service_rates 
            if sr.get('service_id') == service_id
        }
        
        # Combine zone definitions with service rates
        legacy_zones = []
        for zone in zones:
            zone_id = zone.get('id')
            rate_data = service_rate_map.get(zone_id, {})
            
            legacy_zone = {
                **zone,  # Zone definition (label, cities, country_codes, etc.)
                'rate': rate_data.get('rate', 0),
                'min_weight': rate_data.get('min_weight'),
                'max_weight': rate_data.get('max_weight'),
                'transit_days': rate_data.get('transit_days'),
                'transit_time': rate_data.get('transit_time'),
            }
            legacy_zones.append(legacy_zone)
        
        return legacy_zones
    
    def update_service_zone_rate(self, service_id: str, zone_id: str, field: str, value):
        """
        Update a rate field for a specific service-zone combination
        """
        allowed_fields = {
            'rate': float,
            'min_weight': float,
            'max_weight': float,
            'transit_days': int,
            'transit_time': float,
        }
        
        if field not in allowed_fields:
            raise ValueError(f"Field '{field}' is not allowed for rate updates")
        
        # Validate value
        try:
            if value is not None and value != '':
                value = allowed_fields[field](value)
        except (ValueError, TypeError):
            raise ValueError(f"Invalid value '{value}' for field '{field}'")
        
        service_rates = list(self.service_rates or [])
        
        # Find existing rate record
        for rate_record in service_rates:
            if (rate_record.get('service_id') == service_id and 
                rate_record.get('zone_id') == zone_id):
                rate_record[field] = value
                break
        else:
            # Create new rate record
            service_rates.append({
                'service_id': service_id,
                'zone_id': zone_id,
                field: value
            })
        
        self.service_rates = service_rates
        self.save(update_fields=['service_rates'])
    
    def batch_update_service_rates(self, updates):
        """
        Batch update service rates
        updates format: [{'service_id': str, 'zone_id': str, 'field': str, 'value': any}]
        """
        allowed_fields = {
            'rate': float,
            'min_weight': float,
            'max_weight': float, 
            'transit_days': int,
            'transit_time': float,
        }
        
        service_rates = list(self.service_rates or [])
        service_rate_map = {}
        
        # Create lookup map for existing rates
        for i, rate in enumerate(service_rates):
            key = f"{rate.get('service_id')}:{rate.get('zone_id')}"
            service_rate_map[key] = i
        
        for update in updates:
            service_id = update.get('service_id')
            zone_id = update.get('zone_id')
            field = update.get('field')
            value = update.get('value')
            
            if field not in allowed_fields:
                continue
            
            # Validate value
            try:
                if value is not None and value != '':
                    value = allowed_fields[field](value)
            except (ValueError, TypeError):
                continue
            
            key = f"{service_id}:{zone_id}"
            
            if key in service_rate_map:
                # Update existing rate
                service_rates[service_rate_map[key]][field] = value
            else:
                # Create new rate record
                new_rate = {
                    'service_id': service_id,
                    'zone_id': zone_id,
                    field: value
                }
                service_rates.append(new_rate)
                service_rate_map[key] = len(service_rates) - 1
        
        self.service_rates = service_rates
        self.save(update_fields=['service_rates'])
    
    def add_zone(self, zone_data):
        """
        Add a new shared zone definition
        """
        zones = list(self.zones or [])
        
        # Generate zone ID if not provided
        if not zone_data.get('id'):
            zone_data['id'] = f"zone_{len(zones) + 1}"
        
        zones.append(zone_data)
        self.zones = zones
        self.save(update_fields=['zones'])
        return zone_data['id']
    
    def remove_zone(self, zone_id: str):
        """
        Remove a zone and all its associated rates
        """
        # Remove zone definition
        zones = [z for z in (self.zones or []) if z.get('id') != zone_id]
        self.zones = zones
        
        # Remove all rates for this zone
        service_rates = [sr for sr in (self.service_rates or []) if sr.get('zone_id') != zone_id]
        self.service_rates = service_rates
        
        self.save(update_fields=['zones', 'service_rates'])
    
    def migrate_from_legacy_format(self):
        """
        Migrate from old format where zones are stored per service to new shared format
        """
        if self.zones or self.service_rates:
            # Already in new format
            return
        
        all_zones = {}
        service_rates = []
        zone_counter = 1
        
        # Extract unique zones across all services
        for service in self.services.all():
            service_zones = service.zones or []
            
            for zone_index, zone_data in enumerate(service_zones):
                # Create zone signature for deduplication
                zone_signature = {
                    'label': zone_data.get('label', f'Zone {zone_index + 1}'),
                    'cities': sorted(zone_data.get('cities', [])),
                    'postal_codes': sorted(zone_data.get('postal_codes', [])),
                    'country_codes': sorted(zone_data.get('country_codes', [])),
                }
                
                # Use signature as key for deduplication
                sig_key = str(zone_signature)
                
                if sig_key not in all_zones:
                    zone_id = f"zone_{zone_counter}"
                    all_zones[sig_key] = {
                        'id': zone_id,
                        **zone_signature
                    }
                    zone_counter += 1
                
                zone_id = all_zones[sig_key]['id']
                
                # Store service rate
                service_rates.append({
                    'service_id': service.id,
                    'zone_id': zone_id,
                    'rate': zone_data.get('rate', 0),
                    'min_weight': zone_data.get('min_weight'),
                    'max_weight': zone_data.get('max_weight'),
                    'transit_days': zone_data.get('transit_days'),
                    'transit_time': zone_data.get('transit_time'),
                })
        
        # Save optimized structure
        self.zones = list(all_zones.values())
        self.service_rates = service_rates
        self.save(update_fields=['zones', 'service_rates'])