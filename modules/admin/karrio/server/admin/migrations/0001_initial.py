from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="TaskExecution",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("task_id", models.CharField(db_index=True, max_length=255)),
                ("task_name", models.CharField(db_index=True, max_length=255)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("queued", "Queued"),
                            ("executing", "Executing"),
                            ("complete", "Complete"),
                            ("error", "Error"),
                            ("retrying", "Retrying"),
                            ("revoked", "Revoked"),
                            ("expired", "Expired"),
                        ],
                        db_index=True,
                        max_length=20,
                    ),
                ),
                ("queued_at", models.DateTimeField(blank=True, null=True)),
                ("started_at", models.DateTimeField(blank=True, null=True)),
                ("completed_at", models.DateTimeField(blank=True, null=True)),
                ("duration_ms", models.IntegerField(blank=True, null=True)),
                ("error", models.TextField(blank=True, null=True)),
                ("retries", models.IntegerField(default=0)),
                ("args_summary", models.TextField(blank=True, null=True)),
            ],
            options={
                "db_table": "admin_task_execution",
                "ordering": ["-queued_at"],
                "indexes": [
                    models.Index(
                        fields=["-queued_at"],
                        name="admin_task_e_queued__b1c3e3_idx",
                    ),
                    models.Index(
                        fields=["status", "-queued_at"],
                        name="admin_task_e_status_5a8f2c_idx",
                    ),
                    models.Index(
                        fields=["task_name", "-queued_at"],
                        name="admin_task_e_task_na_d4e1f7_idx",
                    ),
                ],
            },
        ),
    ]
