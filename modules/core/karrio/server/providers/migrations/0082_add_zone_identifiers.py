# Generated migration to add unique identifiers to ServiceLevel zones
from django.db import migrations
import uuid


def add_zone_identifiers(apps, schema_editor):
    """Add unique IDs to existing zones in ServiceLevel objects"""
    ServiceLevel = apps.get_model('providers', 'ServiceLevel')
    
    for service in ServiceLevel.objects.all():
        if service.zones:
            updated = False
            for i, zone in enumerate(service.zones):
                if 'id' not in zone:
                    # Generate unique zone ID
                    zone['id'] = f"zone_{uuid.uuid4().hex[:8]}"
                    updated = True
            
            if updated:
                service.save(update_fields=['zones'])


def reverse_zone_identifiers(apps, schema_editor):
    """Remove zone IDs (for rollback)"""
    ServiceLevel = apps.get_model('providers', 'ServiceLevel')
    
    for service in ServiceLevel.objects.all():
        if service.zones:
            updated = False
            for zone in service.zones:
                if 'id' in zone:
                    del zone['id']
                    updated = True
            
            if updated:
                service.save(update_fields=['zones'])


class Migration(migrations.Migration):

    dependencies = [
        ('providers', '0081_remove_alliedexpresssettings_carrier_ptr_and_more'),
    ]

    operations = [
        migrations.RunPython(
            add_zone_identifiers,
            reverse_zone_identifiers
        ),
    ]