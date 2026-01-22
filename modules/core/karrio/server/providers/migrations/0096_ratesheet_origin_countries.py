# Generated migration for RateSheet origin_countries field

from django.db import migrations, models
import karrio.server.core.models


class Migration(migrations.Migration):

    dependencies = [
        ("providers", "0095_rename_carrier_to_carrierconnection"),
    ]

    operations = [
        migrations.AddField(
            model_name="ratesheet",
            name="origin_countries",
            field=models.JSONField(
                blank=True,
                null=True,
                default=karrio.server.core.models.field_default([]),
                help_text="List of origin country codes this rate sheet applies to",
            ),
        ),
    ]
