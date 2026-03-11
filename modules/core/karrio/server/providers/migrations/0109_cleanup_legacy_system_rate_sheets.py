from django.db import migrations


def cleanup_legacy_system_rate_sheets(apps, schema_editor):
    """Delete legacy RateSheet rows that were migrated to SystemRateSheet.

    Runs after providers.0107 switches SystemConnection.rate_sheet FK to
    SystemRateSheet, so deleting legacy rows cannot null SystemConnection FK.
    Also runs after providers.0108 (DHL Parcel DE credential cleanup).
    """
    RateSheet = apps.get_model("providers", "RateSheet")
    SystemRateSheet = apps.get_model("providers", "SystemRateSheet")

    system_ids = list(SystemRateSheet.objects.values_list("id", flat=True))
    if not system_ids:
        return

    deleted, _ = RateSheet.objects.filter(id__in=system_ids).delete()
    if deleted:
        print(
            f"\n  Cleanup: deleted {deleted} legacy RateSheet row(s) "
            f"migrated to SystemRateSheet"
        )


class Migration(migrations.Migration):

    dependencies = [
        ("providers", "0108_clear_dhl_parcel_de_username_password"),
    ]

    operations = [
        migrations.RunPython(
            cleanup_legacy_system_rate_sheets,
            reverse_code=migrations.RunPython.noop,
        ),
    ]
