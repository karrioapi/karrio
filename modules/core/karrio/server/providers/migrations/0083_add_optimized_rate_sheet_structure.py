# Generated migration to add optimized rate sheet structure

from django.db import migrations, models
import karrio.server.core.models as core


class Migration(migrations.Migration):
    dependencies = [
        ('providers', '0082_add_zone_identifiers'),
    ]

    operations = [
        migrations.AddField(
            model_name='ratesheet',
            name='zones',
            field=models.JSONField(
                blank=True,
                null=True,
                default=core.field_default([]),
                help_text="Shared zone definitions: [{'id': 'zone_1', 'label': 'Zone 1', 'cities': [...], 'country_codes': [...]}]"
            ),
        ),
        migrations.AddField(
            model_name='ratesheet',
            name='service_rates',
            field=models.JSONField(
                blank=True,
                null=True,
                default=core.field_default([]),
                help_text="Service-zone rate mapping: [{'service_id': 'svc_1', 'zone_id': 'zone_1', 'rate': 10.50}]"
            ),
        ),
    ]