import functools

import karrio.server.core.models
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("providers", "0111_carrier_options_frozen_connection_type"),
    ]

    operations = [
        migrations.AddField(
            model_name="servicelevel",
            name="tags",
            field=models.JSONField(
                blank=True,
                default=functools.partial(karrio.server.core.models._identity, value={}),
                help_text=(
                    "Curated tag map driven by TAG_REGISTRY: "
                    "{recommended, recommendation_category, recommendation_type, "
                    "display_priority, surface_visibility}"
                ),
                null=True,
            ),
        ),
    ]
