# Generated migration for Markup and Fee models

import functools
from django.db import migrations, models
import django.db.models.deletion
import karrio.server.core.models


class Migration(migrations.Migration):
    """
    Create new Markup and Fee models.

    This is part of the Surcharge -> Markup refactoring:
    - Markup model replaces Surcharge with JSONField-based filters
    - Fee model tracks applied markups for usage statistics
    """

    dependencies = [
        ("pricing", "0075_alter_surcharge_carriers_alter_surcharge_services"),
        ("manager", "0079_remove_carrier_fk_fields"),
    ]

    operations = [
        # Create Markup model
        migrations.CreateModel(
            name="Markup",
            fields=[
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True),
                ),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True),
                ),
                (
                    "id",
                    models.CharField(
                        default=functools.partial(
                            karrio.server.core.models.uuid, prefix="mkp_"
                        ),
                        editable=False,
                        max_length=50,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        help_text="The markup name (label) that will appear in the rate breakdown",
                        max_length=100,
                        unique=True,
                    ),
                ),
                (
                    "active",
                    models.BooleanField(
                        default=True,
                        help_text="Whether the markup is active and will be applied to rates",
                    ),
                ),
                (
                    "amount",
                    models.FloatField(
                        default=0.0,
                        help_text="The markup amount or percentage to add to the quote.",
                    ),
                ),
                (
                    "markup_type",
                    models.CharField(
                        choices=[("AMOUNT", "AMOUNT"), ("PERCENTAGE", "PERCENTAGE")],
                        default="AMOUNT",
                        help_text="Determine whether the markup is in percentage or net amount.",
                        max_length=25,
                    ),
                ),
                (
                    "is_visible",
                    models.BooleanField(
                        default=True,
                        help_text="Whether to show this markup in the rate breakdown to users",
                    ),
                ),
                (
                    "carrier_codes",
                    models.JSONField(
                        blank=True,
                        default=list,
                        help_text="List of carrier codes to apply the markup to.",
                    ),
                ),
                (
                    "service_codes",
                    models.JSONField(
                        blank=True,
                        default=list,
                        help_text="List of service codes to apply the markup to.",
                    ),
                ),
                (
                    "connection_ids",
                    models.JSONField(
                        blank=True,
                        default=list,
                        help_text="List of connection IDs to apply the markup to.",
                    ),
                ),
                (
                    "organization_ids",
                    models.JSONField(
                        blank=True,
                        default=list,
                        help_text="List of organization IDs to apply the markup to.",
                    ),
                ),
                (
                    "metadata",
                    models.JSONField(
                        blank=True,
                        default=dict,
                        help_text="Additional metadata for the markup",
                    ),
                ),
            ],
            options={
                "verbose_name": "Markup",
                "verbose_name_plural": "Markups",
                "db_table": "markup",
                "ordering": ["-created_at"],
            },
        ),
        # Create Fee model
        migrations.CreateModel(
            name="Fee",
            fields=[
                (
                    "id",
                    models.CharField(
                        default=functools.partial(
                            karrio.server.core.models.uuid, prefix="fee_"
                        ),
                        editable=False,
                        max_length=50,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        help_text="The fee name at time of application",
                        max_length=100,
                    ),
                ),
                (
                    "amount",
                    models.FloatField(
                        help_text="The fee amount in the shipment's currency",
                    ),
                ),
                (
                    "currency",
                    models.CharField(
                        help_text="Currency code (e.g., USD, EUR)",
                        max_length=3,
                    ),
                ),
                (
                    "markup_type",
                    models.CharField(
                        choices=[("AMOUNT", "AMOUNT"), ("PERCENTAGE", "PERCENTAGE")],
                        help_text="Whether this was a fixed amount or percentage markup",
                        max_length=25,
                    ),
                ),
                (
                    "markup_percentage",
                    models.FloatField(
                        blank=True,
                        help_text="Original percentage if this was a percentage-based markup",
                        null=True,
                    ),
                ),
                (
                    "carrier_code",
                    models.CharField(
                        help_text="Carrier code at time of shipment creation",
                        max_length=50,
                    ),
                ),
                (
                    "service_code",
                    models.CharField(
                        blank=True,
                        help_text="Service code at time of shipment creation",
                        max_length=100,
                        null=True,
                    ),
                ),
                (
                    "connection_id",
                    models.CharField(
                        help_text="Connection ID used for this shipment",
                        max_length=50,
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True),
                ),
                (
                    "markup",
                    models.ForeignKey(
                        blank=True,
                        help_text="The markup that generated this fee",
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="fees",
                        to="pricing.markup",
                    ),
                ),
                (
                    "shipment",
                    models.ForeignKey(
                        help_text="The shipment this fee was applied to",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="fees",
                        to="manager.shipment",
                    ),
                ),
            ],
            options={
                "verbose_name": "Fee",
                "verbose_name_plural": "Fees",
                "db_table": "fee",
                "ordering": ["-created_at"],
            },
        ),
        # Add indexes for Fee model
        migrations.AddIndex(
            model_name="fee",
            index=models.Index(fields=["shipment_id"], name="fee_shipmen_d4e9f2_idx"),
        ),
        migrations.AddIndex(
            model_name="fee",
            index=models.Index(fields=["markup_id"], name="fee_markup__29f8a1_idx"),
        ),
        migrations.AddIndex(
            model_name="fee",
            index=models.Index(fields=["carrier_code"], name="fee_carrier_3c7b8e_idx"),
        ),
        migrations.AddIndex(
            model_name="fee",
            index=models.Index(fields=["created_at"], name="fee_created_a1b2c3_idx"),
        ),
    ]
