"""
Pricing module signals.

This module provides:
1. Rate post-processing to apply custom markups to shipping quotes
2. Fee capture after shipment label creation
"""

import functools
import importlib
from django.db.models import Q
from django.db.models.signals import post_save
from django.dispatch import receiver

from karrio.server.serializers import Context
from karrio.server.core.gateway import Rates
from karrio.server.core.logging import logger
import karrio.server.pricing.models as models


# ─────────────────────────────────────────────────────────────────────────────
# RATE POST-PROCESSING (Apply markups to quotes)
# ─────────────────────────────────────────────────────────────────────────────


def register_rate_post_processing(*args, **kwargs):
    """Register the markup application function for rate post-processing."""
    Rates.post_process_functions += [apply_custom_markups]
    logger.info("Markup rate post-processing registered", module="karrio.pricing")


def apply_custom_markups(context: Context, result):
    """
    Apply active markups to rate quotes.

    This function is called after rates are fetched from carriers.
    It applies all active markups that match the organization context.

    Markup scoping via organization_ids JSONField:
    - Markups with org ID in organization_ids apply only to that org
    - Markups with empty organization_ids are system-wide
    """
    org_id = getattr(context.org, "id", None)

    if org_id:
        # Filter markups that either:
        # 1. Have the current organization in their organization_ids list
        # 2. Have an empty organization_ids list (system-wide markups)
        _filters = (
            Q(active=True, organization_ids__contains=[org_id])
            | Q(active=True, organization_ids=[]),
        )
    else:
        # No organization context - only apply system-wide markups
        _filters = (Q(active=True, organization_ids=[]),)

    markups = models.Markup.objects.filter(*_filters)

    return functools.reduce(
        lambda cumulated_result, markup: markup.apply_charge(cumulated_result),
        markups,
        result,
    )


# ─────────────────────────────────────────────────────────────────────────────
# FEE CAPTURE (Record fees after shipment creation)
# ─────────────────────────────────────────────────────────────────────────────


def capture_fees_for_shipment(shipment):
    """
    Capture fee records for all markups applied to a shipment.

    This function extracts markup charges from the shipment's selected_rate
    and creates Fee snapshot records for usage statistics and reporting.
    All fields are captured as plain values (no FK references).
    """
    if not shipment.selected_rate:
        return

    selected_rate = shipment.selected_rate
    extra_charges = selected_rate.get("extra_charges", [])
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

    for charge in extra_charges:
        charge_id = charge.get("id")

        # Only capture charges that have IDs starting with 'mkp_' (our markups)
        # or 'chrg_' (legacy surcharges)
        if not charge_id or not (charge_id.startswith("mkp_") or charge_id.startswith("chrg_")):
            continue

        # Look up markup for fee_type/percentage snapshot
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
        if instance.selected_rate and instance.status not in ["draft", "created"]:
            # Check if we've already captured fees for this shipment
            if not models.Fee.objects.filter(shipment_id=instance.id).exists():
                capture_fees_for_shipment(instance)

    logger.info("Fee capture signal registered", module="karrio.pricing")


