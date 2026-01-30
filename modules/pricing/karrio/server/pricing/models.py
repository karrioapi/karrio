import typing
import functools
import django.db.models as models
import django.core.validators as validators
from django.contrib.contenttypes.fields import GenericRelation

import karrio.lib as lib
import karrio.core.models as karrio
import karrio.server.core.models as core
import karrio.server.core.datatypes as datatypes
import karrio.server.providers.models as providers
from karrio.server.core.logging import logger


# ─────────────────────────────────────────────────────────────────────────────
# MARKUP TYPE ENUM
# ─────────────────────────────────────────────────────────────────────────────

MARKUP_TYPE_CHOICES = [
    ("AMOUNT", "AMOUNT"),
    ("PERCENTAGE", "PERCENTAGE"),
]


# ─────────────────────────────────────────────────────────────────────────────
# MARKUP MODEL (replaces Surcharge)
# ─────────────────────────────────────────────────────────────────────────────


@core.register_model
class Markup(core.Entity):
    """
    Flexible markup/surcharge applied to shipping rates.

    This is an admin-managed model (no user-level access control).
    Use organization_ids JSONField to scope markups to specific organizations.
    An empty organization_ids list means the markup applies system-wide.

    Key changes from legacy Surcharge:
    - Renamed from Surcharge to Markup
    - Uses string lists instead of M2M/FK/enum relations
    - connection_ids supports all connection types (account, system, brokered)
    - carrier_codes and service_codes are validated strings, not enums
    """

    class Meta:
        db_table = "markup"
        verbose_name = "Markup"
        verbose_name_plural = "Markups"
        ordering = ["-created_at"]

    id = models.CharField(
        max_length=50,
        primary_key=True,
        default=functools.partial(core.uuid, prefix="mkp_"),
        editable=False,
    )
    name = models.CharField(
        max_length=100,
        unique=True,
        help_text="The markup name (label) that will appear in the rate breakdown",
    )
    active = models.BooleanField(
        default=True,
        help_text="Whether the markup is active and will be applied to rates",
    )
    amount = models.FloatField(
        validators=[validators.MinValueValidator(0.0)],
        default=0.0,
        help_text="""
        The markup amount or percentage to add to the quote.
        For AMOUNT type: the exact dollar amount to add.
        For PERCENTAGE type: the percentage (e.g., 5 means 5%).
        """,
    )
    markup_type = models.CharField(
        max_length=25,
        choices=MARKUP_TYPE_CHOICES,
        default=MARKUP_TYPE_CHOICES[0][0],
        help_text="""
        Determine whether the markup is in percentage or net amount.
        AMOUNT: rate ($22) + amount (1) = $23
        PERCENTAGE: rate ($22) * 5% = $23.10
        """,
    )
    is_visible = models.BooleanField(
        default=True,
        help_text="Whether to show this markup in the rate breakdown to users",
    )

    # Filters (all string lists, validated on save)
    carrier_codes = models.JSONField(
        default=list,
        blank=True,
        help_text="""
        List of carrier codes to apply the markup to (e.g., ["fedex", "ups"]).
        Empty list means apply to all carriers.
        """,
    )
    service_codes = models.JSONField(
        default=list,
        blank=True,
        help_text="""
        List of service codes to apply the markup to (e.g., ["fedex_ground", "ups_next_day"]).
        Empty list means apply to all services.
        """,
    )
    connection_ids = models.JSONField(
        default=list,
        blank=True,
        help_text="""
        List of connection IDs to apply the markup to (e.g., ["car_xxx", "car_yyy"]).
        Supports all connection types: CarrierConnection, SystemConnection, BrokeredConnection.
        Empty list means apply to all connections.
        """,
    )
    organization_ids = models.JSONField(
        default=list,
        blank=True,
        help_text="""
        List of organization IDs to apply the markup to.
        Empty list means apply to all organizations (system-wide).
        """,
    )

    # Metadata
    metadata = models.JSONField(
        default=dict,
        blank=True,
        help_text="Additional metadata for the markup",
    )

    # Metafields via GenericRelation
    metafields = GenericRelation(
        "core.Metafield",
        related_query_name="markup",
    )

    @property
    def object_type(self):
        return "markup"

    def __str__(self):
        type_ = "$" if self.markup_type == "AMOUNT" else "%"
        return f"{self.name} ({self.amount}{type_})"

    def _is_applicable(self, rate: datatypes.Rate) -> bool:
        """Check if this markup should be applied to the given rate."""
        applicable = []

        # Check carrier code filter
        if self.carrier_codes:
            # For custom carriers (ext="generic"), check if "generic" is in the carrier list
            if (
                rate.meta
                and rate.meta.get("ext") == "generic"
                and "generic" in self.carrier_codes
            ):
                applicable.append(True)
            else:
                applicable.append(rate.carrier_name in self.carrier_codes)

        # Check connection ID filter
        if self.connection_ids:
            connection_id = rate.meta.get("carrier_connection_id") if rate.meta else None
            applicable.append(connection_id in self.connection_ids)

        # Check service code filter
        if self.service_codes:
            applicable.append(rate.service in self.service_codes)

        # All specified filters must match (AND logic)
        # If no filters specified (all empty), markup applies to all rates
        return (not applicable) or (any(applicable) and all(applicable))

    def apply_charge(self, response: datatypes.RateResponse) -> datatypes.RateResponse:
        """Apply this markup to all applicable rates in the response."""

        def apply(rate: datatypes.Rate) -> datatypes.Rate:
            if not self._is_applicable(rate):
                return rate

            logger.debug(
                "Applying markup to rate",
                rate_id=rate.id,
                markup_id=self.id,
                markup_name=self.name,
            )

            amount = lib.to_decimal(
                self.amount
                if self.markup_type == "AMOUNT"
                else (rate.total_charge * (typing.cast(float, self.amount) / 100))
            )
            total_charge = lib.to_decimal(rate.total_charge + amount)
            extra_charges = rate.extra_charges + [
                karrio.ChargeDetails(
                    name=typing.cast(str, self.name),
                    amount=amount,
                    currency=rate.currency,
                    id=self.id,
                )
            ]

            return datatypes.Rate(
                **{
                    **lib.to_dict(rate),
                    "total_charge": total_charge,
                    "extra_charges": extra_charges,
                }
            )

        return datatypes.RateResponse(
            messages=response.messages,
            rates=sorted(
                [apply(rate) for rate in response.rates],
                key=lambda rate: rate.total_charge,
            ),
        )


# ─────────────────────────────────────────────────────────────────────────────
# FEE MODEL (tracks applied markups for usage statistics)
# ─────────────────────────────────────────────────────────────────────────────


class Fee(models.Model):
    """
    Immutable snapshot of an applied fee at time of shipment purchase.
    Primary source of truth for usage statistics and financial reporting.

    All reference fields are plain CharFields (no FKs) — this decouples
    fee records from live objects so they survive deletions/changes.
    """

    class Meta:
        db_table = "fee"
        verbose_name = "Fee"
        verbose_name_plural = "Fees"
        ordering = ["-created_at"]
        indexes = [
            # Single-field indexes for fields without db_index=True
            models.Index(fields=["carrier_code"]),
            models.Index(fields=["created_at"]),
            # Composite indexes for time-series queries
            models.Index(fields=["account_id", "created_at"]),
            models.Index(fields=["connection_id", "created_at"]),
            models.Index(fields=["markup_id", "created_at"]),
        ]

    id = models.CharField(
        max_length=50,
        primary_key=True,
        default=functools.partial(core.uuid, prefix="fee_"),
        editable=False,
    )

    # Fee details (captured at time of application)
    name = models.CharField(
        max_length=100,
        help_text="The fee name at time of application",
    )
    amount = models.FloatField(
        help_text="The fee amount in the shipment's currency",
    )
    currency = models.CharField(
        max_length=3,
        help_text="Currency code (e.g., USD, EUR)",
    )
    fee_type = models.CharField(
        max_length=25,
        choices=MARKUP_TYPE_CHOICES,
        help_text="Whether this was a fixed amount or percentage markup",
    )
    percentage = models.FloatField(
        null=True,
        blank=True,
        help_text="Original percentage if this was a percentage-based markup",
    )

    # Markup reference (snapshot, no FK)
    markup_id = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        db_index=True,
        help_text="The markup ID that generated this fee",
    )

    # Shipment reference (snapshot, no FK)
    shipment_id = models.CharField(
        max_length=50,
        db_index=True,
        help_text="The shipment this fee was applied to",
    )

    # Organization/Account reference (snapshot, no FK)
    account_id = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        db_index=True,
        help_text="The organization/account this fee belongs to",
    )

    # Carrier connection context
    connection_id = models.CharField(
        max_length=50,
        db_index=True,
        help_text="Connection ID used for this shipment",
    )
    carrier_code = models.CharField(
        max_length=50,
        help_text="Carrier code at time of shipment creation",
    )
    service_code = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        help_text="Service code at time of shipment creation",
    )

    # Context
    test_mode = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name}: {self.amount} {self.currency}"

    @property
    def object_type(self):
        return "fee"


