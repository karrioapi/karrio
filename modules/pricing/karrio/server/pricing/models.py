import functools

import django.core.validators as validators
import django.db.models as models
import karrio.core.models as karrio
import karrio.lib as lib
import karrio.server.core.datatypes as datatypes
import karrio.server.core.models as core
from django.contrib.contenttypes.fields import GenericRelation
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

    # Structured categorization metadata
    meta = models.JSONField(
        default=dict,
        blank=True,
        help_text="""
        Structured categorization metadata.
        {
            "type": "brokerage-fee",       # brokerage-fee | insurance | surcharge | notification | address-validation
            "plan": "scale",               # Free-form plan/tier name
            "show_in_preview": true,        # Whether to show computed column in rate sheet preview
            "feature_gate": "insurance"    # Optional: service feature key that must be supported AND requested in options
        }
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

    def _is_applicable(self, rate: datatypes.Rate, options: dict = None) -> bool:
        """Check if this markup should be applied to the given rate."""

        # Check per-rate exclusions (from service/rate-sheet pricing_config)
        excluded_ids = (rate.meta or {}).get("excluded_markup_ids", [])
        if self.id in excluded_ids:
            return False

        applicable = []

        # Feature gate check via meta.feature_gate
        # If set, the markup only applies when:
        #   1. The service supports the feature (via service_features in rate.meta)
        #   2. The shipper requests it in options (at runtime)
        feature_key = (self.meta or {}).get("feature_gate")

        if feature_key:
            # Check 1: service supports this feature
            service_features = (rate.meta or {}).get("service_features", [])
            if feature_key not in service_features:
                return False

            # Check 2: option was requested
            request_options = options or {}
            if not request_options.get(feature_key):
                return False

        # Check carrier code filter
        if self.carrier_codes:
            # For custom carriers (ext="generic"), check if "generic" is in the carrier list
            if rate.meta and rate.meta.get("ext") == "generic" and "generic" in self.carrier_codes:
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

    def apply_charge(self, response: datatypes.RateResponse, options: dict = None) -> datatypes.RateResponse:
        """Apply this markup to all applicable rates in the response."""

        def apply(rate: datatypes.Rate) -> datatypes.Rate:
            if not self._is_applicable(rate, options=options):
                return rate

            logger.debug(
                "Applying markup to rate",
                rate_id=rate.id,
                markup_id=self.id,
                markup_name=self.name,
            )

            # Per-rate custom margin override lookup via typed PlanOverride
            # helper. `rate.meta` is the storage dict; PlanOverride.from_dict
            # handles partial/missing shapes.
            from karrio.server.providers.rate_sheet_datatypes import PlanOverride

            rate_meta = getattr(rate, "meta", None) if hasattr(rate, "meta") else None
            if not isinstance(rate_meta, dict):
                rate_meta = None

            # Honor per-rate excluded markups: if this markup is in the
            # rate's meta.excluded_markup_ids list, skip it entirely so the
            # merchant pays only base + surcharges for this specific rate.
            excluded = (rate_meta or {}).get("excluded_markup_ids") or []
            if self.id in excluded:
                return rate

            override = PlanOverride.from_dict(rate_meta)
            override_amount, override_type = override.override_for(self.id)

            # Fallback: CSV imports only know the plan slug (not the markup
            # id at write time) so the flat plan_cost_<slug> / plan_rate_<slug>
            # keys on meta are the authoritative source. Resolve them via
            # this markup's plan slug when the markup-id lookup misses.
            if override_amount is None:
                markup_plan = (self.meta or {}).get("plan") if isinstance(self.meta, dict) else None
                if markup_plan and isinstance(rate_meta, dict):
                    amount_by_slug = rate_meta.get(f"plan_cost_{markup_plan}")
                    percent_by_slug = rate_meta.get(f"plan_rate_{markup_plan}")
                    if amount_by_slug is not None:
                        override_amount, override_type = amount_by_slug, "AMOUNT"
                    elif percent_by_slug is not None:
                        override_amount, override_type = percent_by_slug, "PERCENTAGE"

            effective_type = override_type or self.markup_type
            effective_value = override_amount if override_amount is not None else self.amount

            # PERCENTAGE applies to the CARRIER base rate (pre-markup, pre-
            # surcharge) so the margin is deterministic and doesn't compound
            # with surcharges or prior markups. AMOUNT adds as-is.
            base_rate = float(getattr(rate, "base_charge", None) or rate.total_charge)
            amount = lib.to_decimal(
                effective_value if effective_type == "AMOUNT" else (base_rate * (float(effective_value) / 100))
            )
            total_charge = lib.to_decimal(rate.total_charge + amount)

            # Extra-charges composition:
            #   - Visible markups → appended as their own named line item.
            #   - Invisible markups (plan platform fees) → merged INTO the
            #     existing "Base Charge" entry so the customer sees
            #     base_rate + margin as a single base line. Keeps the
            #     breakdown total consistent with total_charge without
            #     exposing a "Margin" row to the customer.
            if self.is_visible:
                extra_charges = list(rate.extra_charges) + [
                    karrio.ChargeDetails(
                        name=str(self.name),
                        amount=amount,
                        currency=rate.currency,
                        id=self.id,
                    )
                ]
            else:
                extra_charges = []
                base_seen = False
                for c in rate.extra_charges:
                    c_name = (getattr(c, "name", "") or "").strip().lower()
                    if not base_seen and c_name == "base charge":
                        extra_charges.append(
                            karrio.ChargeDetails(
                                name=c.name,
                                amount=lib.to_decimal((c.amount or 0) + amount),
                                currency=c.currency,
                                id=getattr(c, "id", None),
                            )
                        )
                        base_seen = True
                    else:
                        extra_charges.append(c)
                if not base_seen:
                    # No Base Charge line to merge into — skip append so the
                    # invisible markup stays invisible. total_charge already
                    # reflects the added amount above.
                    extra_charges = list(rate.extra_charges)

            # For invisible markups, also update rate.base_charge so callers
            # that read it directly (like the shipping-app price card) see
            # the embedded amount.
            new_base_charge = getattr(rate, "base_charge", None)
            if not self.is_visible and new_base_charge is not None:
                new_base_charge = lib.to_decimal(float(new_base_charge) + float(amount))

            return datatypes.Rate(
                **{
                    **lib.to_dict(rate),
                    "total_charge": total_charge,
                    "extra_charges": extra_charges,
                    **({"base_charge": new_base_charge} if new_base_charge is not None else {}),
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

    id = models.CharField(  # noqa: DJ012
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
    markup_id = models.CharField(  # noqa: DJ001
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
    account_id = models.CharField(  # noqa: DJ001
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
    service_code = models.CharField(  # noqa: DJ001
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
