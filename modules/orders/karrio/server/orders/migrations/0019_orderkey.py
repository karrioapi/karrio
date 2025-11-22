import functools
from django.db import migrations, models

import karrio.server.core.models.base


class Migration(migrations.Migration):

    dependencies = [
        ("orders", "0018_ordercounter"),
    ]

    operations = [
        migrations.CreateModel(
            name="OrderKey",
            fields=[
                (
                    "id",
                    models.CharField(
                        default=functools.partial(
                            karrio.server.core.models.base.uuid,
                            **{"prefix": "okey_"},
                        ),
                        editable=False,
                        max_length=50,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("scope", models.CharField(max_length=50)),
                ("source", models.CharField(default="API", max_length=50)),
                ("order_reference", models.CharField(max_length=50)),
                ("test_mode", models.BooleanField(default=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "order",
                    models.OneToOneField(
                        blank=True,
                        null=True,
                        on_delete=models.CASCADE,
                        related_name="dedup_key",
                        db_column="order_record_id",
                        to="orders.order",
                    ),
                ),
            ],
            options={
                "db_table": "order_key",
                "unique_together": {("scope", "source", "order_reference", "test_mode")},
                "indexes": [
                    models.Index(
                        fields=["scope", "source", "order_reference", "test_mode"],
                        name="order_key_scope_idx",
                    )
                ],
            },
        ),
    ]
