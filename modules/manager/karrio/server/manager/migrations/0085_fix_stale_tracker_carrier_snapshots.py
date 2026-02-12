# Data migration: Fix stale tracker carrier snapshots after system/brokered migration
#
# Migration 0093 (providers) moved system Carriers to SystemConnection and deleted
# the original Carrier records. However, tracker carrier snapshots were never updated,
# leaving them with connection_type="account" and deleted car_* connection IDs.
#
# This migration updates those stale snapshots to point to the correct
# SystemConnection/BrokeredConnection using carrier_code + carrier_id matching.

from django.db import migrations


def fix_stale_tracker_snapshots(apps, schema_editor):
    """
    Find trackers with stale 'account' snapshots (deleted CarrierConnection IDs)
    and update them to reference the corresponding SystemConnection/BrokeredConnection.
    """
    Tracking = apps.get_model("manager", "Tracking")

    try:
        CarrierConnection = apps.get_model("providers", "CarrierConnection")
    except LookupError:
        return

    try:
        SystemConnection = apps.get_model("providers", "SystemConnection")
        BrokeredConnection = apps.get_model("providers", "BrokeredConnection")
    except LookupError:
        # System/Brokered models don't exist yet
        return

    # Get all active CarrierConnection IDs for quick lookup
    active_carrier_ids = set(
        CarrierConnection.objects.filter(active=True).values_list("id", flat=True)
    )

    # Build a lookup: (carrier_code, carrier_id, test_mode) -> sys_connection_id
    system_lookup = {}
    for sc in SystemConnection.objects.filter(active=True):
        key = (sc.carrier_code, sc.carrier_id, sc.test_mode)
        system_lookup[key] = sc.id

    # Find trackers with account connection_type
    stale_trackers = Tracking.objects.filter(
        carrier__connection_type="account",
    ).exclude(
        carrier__connection_id__in=active_carrier_ids,
    )

    updated = 0
    for tracker in stale_trackers.iterator(chunk_size=500):
        snapshot = tracker.carrier or {}
        conn_id = snapshot.get("connection_id")

        # Skip if connection still exists
        if conn_id in active_carrier_ids:
            continue

        carrier_code = snapshot.get("carrier_code")
        carrier_id = snapshot.get("carrier_id")
        test_mode = snapshot.get("test_mode", False)

        if not carrier_code or not carrier_id:
            continue

        # Find matching SystemConnection
        sys_id = system_lookup.get((carrier_code, carrier_id, test_mode))
        if not sys_id:
            continue

        # Update snapshot to brokered type pointing to SystemConnection
        tracker.carrier = {
            **snapshot,
            "connection_id": sys_id,
            "connection_type": "brokered",
        }
        tracker.save(update_fields=["carrier"])
        updated += 1

    if updated:
        print(f"  Updated {updated} tracker carrier snapshots from stale account to brokered")


def reverse_migration(apps, schema_editor):
    # No-op: we can't reliably reverse this since we don't store old connection IDs
    pass


class Migration(migrations.Migration):
    """
    Fix stale tracker carrier snapshots left behind by the system/brokered
    connection migration (providers 0093).
    """

    dependencies = [
        ("manager", "0084_shipment_return_shipment"),
        ("providers", "0095_rename_carrier_to_carrierconnection"),
    ]

    operations = [
        migrations.RunPython(fix_stale_tracker_snapshots, reverse_migration),
    ]
