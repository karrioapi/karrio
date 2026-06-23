"""Backfill the ``paperless`` capability onto pre-existing connections.

Capabilities are computed once, at connection creation, only when empty
(``providers/signals.py::carrier_changed``) — they are never recomputed on
save. So any connection created before its connector gained paperless support
keeps stale capabilities and ``supports_paperless_trade`` silently gates the
whole ETD flow off (no generation, no upload, no traces).

This backfills ``paperless`` onto every existing connection whose connector now
declares it (``ShippingOption.paperless_trade`` with ``meta["category"] ==
"PAPERLESS"``, surfaced via ``references.get_carrier_capabilities``). Mirrors the
``0101_add_pickup_capability_to_dhl_parcel_de`` precedent, generalised across
carriers.

Brokered connections inherit capabilities from their system connection when
``capabilities_overrides`` is empty, so only non-empty overrides need touching.
"""

from django.db import migrations


def _paperless_carrier_codes(carrier_codes) -> set:
    """The subset of carrier_codes whose connector now advertises paperless."""
    import karrio.references as ref

    result = set()
    for code in {c for c in carrier_codes if c}:
        capabilities = ref.get_carrier_capabilities(code) or []
        if "paperless" in capabilities:
            result.add(code)
    return result


def add_paperless_capability(apps, schema_editor):
    db_alias = schema_editor.connection.alias

    # Connections that store capabilities directly.
    for model_name in ("CarrierConnection", "SystemConnection"):
        Model = apps.get_model("providers", model_name)
        codes = _paperless_carrier_codes(
            Model.objects.using(db_alias).values_list("carrier_code", flat=True).distinct()
        )
        for conn in Model.objects.using(db_alias).filter(carrier_code__in=codes).iterator():
            capabilities = conn.capabilities or []
            if "paperless" not in capabilities:
                conn.capabilities = [*capabilities, "paperless"]
                conn.save(update_fields=["capabilities"])

    # Brokered connections inherit from their system connection unless they carry
    # a non-empty override (which REPLACES the inherited set) — only those need it.
    Brokered = apps.get_model("providers", "BrokeredConnection")
    brokered = Brokered.objects.using(db_alias).select_related("system_connection")
    codes = _paperless_carrier_codes(brokered.values_list("system_connection__carrier_code", flat=True).distinct())
    for conn in brokered.iterator():
        overrides = conn.capabilities_overrides or []
        code = conn.system_connection.carrier_code if conn.system_connection_id else None
        if overrides and code in codes and "paperless" not in overrides:
            conn.capabilities_overrides = [*overrides, "paperless"]
            conn.save(update_fields=["capabilities_overrides"])


def remove_paperless_capability(apps, schema_editor):
    db_alias = schema_editor.connection.alias

    for model_name in ("CarrierConnection", "SystemConnection"):
        Model = apps.get_model("providers", model_name)
        for conn in Model.objects.using(db_alias).iterator():
            capabilities = conn.capabilities or []
            if "paperless" in capabilities:
                conn.capabilities = [c for c in capabilities if c != "paperless"]
                conn.save(update_fields=["capabilities"])

    Brokered = apps.get_model("providers", "BrokeredConnection")
    for conn in Brokered.objects.using(db_alias).iterator():
        overrides = conn.capabilities_overrides or []
        if "paperless" in overrides:
            conn.capabilities_overrides = [c for c in overrides if c != "paperless"]
            conn.save(update_fields=["capabilities_overrides"])


class Migration(migrations.Migration):
    dependencies = [
        ("providers", "0113_alter_brokeredconnection_capabilities_overrides_and_more"),
    ]

    operations = [
        migrations.RunPython(add_paperless_capability, remove_paperless_capability),
    ]
