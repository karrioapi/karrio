from django.db import migrations, models
from django.db.models.fields import json


class Migration(migrations.Migration):

    dependencies = [
        ("tracing", "0007_tracingrecord_tracing_created_at_idx"),
    ]

    operations = [
        migrations.AddIndex(
            model_name="tracingrecord",
            index=models.Index(
                json.KeyTextTransform("request_id", "meta"),
                condition=models.Q(meta__request_id__isnull=False),
                name="request_id_idx",
            ),
        ),
    ]
