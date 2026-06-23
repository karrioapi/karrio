"""
Pricing module signals.

This module provides:
1. Rate post-processing to apply custom markups to shipping quotes
2. Fee capture after shipment label creation
"""

import functools
import typing

import karrio.lib as lib
import karrio.server.pricing.models as models
from django.db.models import Q
from django.db.models.signals import post_save
from django.dispatch import receiver
from karrio.server.core.gateway import Rates
from karrio.server.core.logging import logger

# Hook point: extension modules append `(context) -> str | None` callables
# in their `AppConfig.ready()` to resolve the tenant's current plan tier.
# Used by the rate-quote-time markup filter (`apply_custom_markups`). The
# first resolver that returns a truthy string wins.
#
# Why a hook instead of a direct import: plan resolution is JTL-specific
# (entitlement service, system_metadata fallbacks). Karrio core stays
# generic and any extension wanting plan-tier-scoped markups registers
# its own resolver.
plan_resolvers: list[typing.Callable[[typing.Any], str | None]] = []


def _resolve_tenant_plan(context: typing.Any) -> str | None:
    """Run every registered resolver and return the first truthy plan slug."""
    for resolver in plan_resolvers:
        plan = lib.failsafe(lambda r=resolver: r(context))
        if isinstance(plan, str) and plan:
            return plan
    return None


# ─────────────────────────────────────────────────────────────────────────────
# RATE POST-PROCESSING (Apply markups to quotes)
# ─────────────────────────────────────────────────────────────────────────────


def register_rate_post_processing(*args, **kwargs):
    """Register the markup application function for rate post-processing."""
    Rates.hooks.after("fetch", apply_custom_markups)
    Rates.hooks.after("resolve", apply_custom_markups)
    logger.info("Markup rate post-processing registered", module="karrio.pricing")


def apply_custom_markups(result, *args, **kwargs):
    """
    Apply active markups to rate quotes.

    This function is called as an after-hook on Rates.fetch/resolve.
    It applies all active markups that match the organization context
    and the tenant's pricing plan.

    Markup scoping via organization_ids JSONField:
    - Markups with org ID in organization_ids apply only to that org
    - Markups with empty organization_ids are system-wide

    Plan filtering via meta.plan:
    - Markups with no plan in meta are global (apply to all plans)
    - Markups with meta.plan only apply when the tenant's plan matches
    - Plan is resolved via get_plan() (ES → org.system_metadata["plan"] → "start")
    """
    context = kwargs.get("context")
    if context is None:
        return result

    # Live-carrier rates (Rates.fetch path) come back with carrier-side meta
    # only — no plan_costs from the rate sheet. Without this enrichment,
    # Markup.apply_charge falls through to Markup.amount, which is 0.0 on
    # plan-tier markups by design (per-row plan_costs are authoritative).
    # The resolver path already carries plan_costs on rate.meta — this
    # brings the live-carrier path into parity with it.
    from karrio.server.pricing.rate_enrichment import (
        enrich_brokered_rates_with_sheet_meta,
    )

    payload = args[0] if args else kwargs.get("payload")
    enrich_brokered_rates_with_sheet_meta(result, payload)

    org_id = getattr(context.org, "id", None)

    if org_id:
        # Filter markups that either:
        # 1. Have the current organization in their organization_ids list
        # 2. Have an empty organization_ids list (system-wide markups)
        # Note: icontains is used instead of __contains for cross-DB
        # compatibility (SQLite does not support JSON containment lookups).
        _filters = (Q(active=True, organization_ids__icontains=org_id) | Q(active=True, organization_ids=[]),)
    else:
        # No organization context - only apply system-wide markups
        _filters = (Q(active=True, organization_ids=[]),)

    markups = models.Markup.objects.filter(*_filters)

    tenant_plan = _resolve_tenant_plan(context)

    context_data = None
    if hasattr(context, "_full_data"):
        context_data = context._full_data
    elif hasattr(context, "data"):
        context_data = context.data

    # Filter markups by plan:
    # Apply if markup has no plan in meta (global) OR plan matches tenant's plan
    # Note: plan is stored in meta (structured categorization), NOT metadata
    def matches_plan(markup):
        markup_plan = (markup.meta or {}).get("plan")
        return markup_plan is None or markup_plan == tenant_plan

    # Extract request options for feature-gated markup checks
    request_options = {}
    if context_data:
        request_options = context_data.get("options") or {}

    applicable_markups = [m for m in markups if matches_plan(m)]

    applied_result = functools.reduce(
        lambda cumulated_result, markup: markup.apply_charge(cumulated_result, options=request_options),
        applicable_markups,
        result,
    )

    # Scrub non-active-plan data from rate.meta + stamp the active plan so
    # downstream consumers (admin preview, billing, merchant rate cards) see
    # a single authoritative plan per rate. Same behavior as the shipping
    # method rate resolver's `_apply_markups_to_rates` — the two paths must
    # produce structurally identical rates.
    #
    # Only runs when a plan-scoped markup was evaluated for this tenant;
    # otherwise we leave meta untouched so rates that never touch the plan
    # system don't get spurious `plan` / scrubbed `plan_costs` keys.
    has_plan_markup = any((m.meta or {}).get("plan") for m in applicable_markups)
    if tenant_plan and has_plan_markup and hasattr(applied_result, "rates"):
        active_markup_ids = {m.id for m in applicable_markups if (m.meta or {}).get("plan") == tenant_plan}
        unscoped_markup_ids = {m.id for m in applicable_markups if not (m.meta or {}).get("plan")}
        keep_ids = active_markup_ids | unscoped_markup_ids
        for rate in applied_result.rates:
            rate_meta = getattr(rate, "meta", None)
            if not isinstance(rate_meta, dict):
                continue
            pc = rate_meta.get("plan_costs")
            if isinstance(pc, dict):
                rate_meta["plan_costs"] = {k: v for k, v in pc.items() if k in keep_ids}
            pct = rate_meta.get("plan_cost_types")
            if isinstance(pct, dict):
                rate_meta["plan_cost_types"] = {k: v for k, v in pct.items() if k in keep_ids}
            # Strip flat `plan_cost_<slug>` / `plan_rate_<slug>` extras for
            # non-active tiers. Exclude the structured `plan_costs` /
            # `plan_cost_types` dicts themselves — those were already
            # scrubbed above and must not be popped by the slug loop.
            reserved = {"plan_costs", "plan_cost_types", "plan_rates", "plan_rate_types"}
            for k in list(rate_meta):
                if k in reserved:
                    continue
                if k.startswith("plan_cost_") or k.startswith("plan_rate_"):
                    slug = k.split("_", 2)[-1]
                    if slug != tenant_plan:
                        rate_meta.pop(k, None)
            rate_meta["plan"] = tenant_plan

    return applied_result


# ─────────────────────────────────────────────────────────────────────────────
# FEE CAPTURE (Record fees after shipment creation)
# ─────────────────────────────────────────────────────────────────────────────


def capture_fees_for_shipment(shipment):
    """
    Capture fee records for all markups applied to a shipment.

    This function extracts markup charges from the shipment's selected_rate
    and creates Fee snapshot records for usage statistics and reporting.
    All fields are captured as plain values (no FK references).

    Reads the typed charge breakdown (charge_type "markup" / "platform_fee")
    and falls back to the `normalize_extra_charges` adapter for shipments
    written before the typed-breakdown migration.
    """
    if not shipment.selected_rate:
        return

    from karrio.server.pricing.charge_breakdown import MARGIN_CHARGE_TYPES, normalize_extra_charges

    selected_rate = shipment.selected_rate
    meta = selected_rate.get("meta", {}) or {}
    carrier_code = meta.get("carrier_code") or selected_rate.get("carrier_name", "")
    service_code = selected_rate.get("service", "")
    connection_id = meta.get("carrier_connection_id", "") or meta.get("connection_id", "")
    currency = selected_rate.get("currency", "USD")
    test_mode = getattr(shipment, "test_mode", False)

    # Resolve account/org ID from shipment's org link
    account_id = None
    if hasattr(shipment, "org"):
        _org = shipment.org.first()
        account_id = getattr(_org, "id", None)

    # Read the plan tier from the purchase-time snapshot frozen on
    # shipment.meta by `purchase_meta_writers` (manager core hook).
    # Legacy shipments missing the snapshot get None — falling back to
    # `get_plan(org)` here would pull the org's *current* plan tier and
    # mis-reconstruct historical fees if the tier has changed since.
    snapshot_plan = (getattr(shipment, "meta", None) or {}).get("plan_at_purchase")
    org_plan = snapshot_plan if isinstance(snapshot_plan, str) and snapshot_plan else None

    # Defer capture until the org link is in place.
    # The post_save signal fires on the very first Shipment.objects.create()
    # — BEFORE `@owned_model_serializer.link_org` writes the ShipmentLink row.
    # Fee rows captured at that moment have `account_id=NULL`, which makes
    # them invisible to the admin `total_addons_charges` aggregation
    # (filters on `account_id=<org_id>`). Skipping here is safe because
    # `buy_shipment_label` issues another `shipment.save()` after the link
    # is written; the dedup guard in `on_shipment_saved` (no existing Fee)
    # then admits the signal and capture runs with the correct account_id.
    if account_id is None:
        logger.debug("Deferring fee capture for shipment %s — org not yet linked", shipment.id)
        return

    extra_charges = normalize_extra_charges(selected_rate, org_plan=org_plan)

    # Per-shipment dedupe: capture each markup at most once even if the
    # adapter ever emits the same `id` twice (legacy bug) or the signal
    # fires multiple times during the buy_shipment_label save sequence.
    seen_markup_ids: set[str] = set()
    existing_markup_ids = set(models.Fee.objects.filter(shipment_id=shipment.id).values_list("markup_id", flat=True))

    for charge in extra_charges:
        if charge.get("charge_type") not in MARGIN_CHARGE_TYPES:
            continue

        charge_id = charge.get("id")
        if not charge_id:
            # Adapter-synthesized platform_fee without a recoverable
            # markup id — skip rather than write a Fee row we cannot
            # link back to a Markup for reporting.
            continue

        if charge_id in seen_markup_ids or charge_id in existing_markup_ids:
            continue
        seen_markup_ids.add(charge_id)

        markup = models.Markup.objects.filter(id=charge_id).first()

        # Create fee snapshot record (no FK references)
        try:
            models.Fee.objects.create(
                shipment_id=shipment.id,
                markup_id=charge_id,
                account_id=account_id,
                test_mode=test_mode,
                name=charge.get("name", ""),
                amount=charge.get("amount", 0),
                currency=currency,
                fee_type=markup.markup_type if markup else "AMOUNT",
                percentage=markup.amount if markup and markup.markup_type == "PERCENTAGE" else None,
                carrier_code=carrier_code,
                service_code=service_code,
                connection_id=connection_id,
            )
            logger.debug(
                "Fee captured for shipment",
                shipment_id=shipment.id,
                markup_id=charge_id,
                amount=charge.get("amount"),
            )
        except Exception as e:
            logger.warning(
                "Failed to capture fee for shipment",
                shipment_id=shipment.id,
                charge_id=charge_id,
                error=str(e),
            )


def register_fee_capture(*args, **kwargs):
    """Register the fee capture signal for shipment post-save."""
    # Import here to avoid circular imports
    import karrio.server.manager.models as manager

    @receiver(post_save, sender=manager.Shipment)
    def on_shipment_saved(sender, instance, created, **kwargs):
        """Capture fees when a shipment is created or updated with a selected rate."""
        # Only capture fees when:
        # 1. Shipment has a selected_rate (label was purchased)
        # 2. Shipment status indicates it's been purchased/processed
        if (
            instance.selected_rate
            and instance.status not in ["draft"]
            and not models.Fee.objects.filter(shipment_id=instance.id).exists()
        ):
            capture_fees_for_shipment(instance)

    logger.info("Fee capture signal registered", module="karrio.pricing")
