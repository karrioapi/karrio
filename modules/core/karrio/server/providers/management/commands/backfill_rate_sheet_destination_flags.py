"""Backfill ServiceLevel.domicile / international from rate-sheet zone coverage.

`domicile` / `international` are DERIVED from each service's resolved zone
coverage vs. the rate sheet's `origin_countries` (see
`data.resources.rate_sheets.derive_destination_flags`). The import path (#717)
derives them on every (re)import, but rate sheets imported BEFORE that fix have
the flags unset (`None`) — so `international`-gated UX (e.g. the shipping-method
Customs/Zoll tab, which only appears for services where `international == True`)
and cross-border rate filtering silently misbehave.

This re-derives the flags for existing rate sheets (tenant `RateSheet` +
`SystemRateSheet`) from their current zones. It is idempotent and deterministic —
safe to re-run; it never trusts stale CSV columns, only the zone definitions.

    karrio run backfill_rate_sheet_destination_flags --dry-run
    karrio run backfill_rate_sheet_destination_flags
"""

from django.core.management.base import BaseCommand
from karrio.server.data.resources.rate_sheets import derive_destination_flags
from karrio.server.providers.models import RateSheet, SystemRateSheet


class Command(BaseCommand):
    help = "Re-derive ServiceLevel.domicile/international from rate-sheet zone coverage (backfill pre-#717 data)."

    def add_arguments(self, parser):
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Report what would change without writing.",
        )

    def handle(self, *args, **options):
        dry_run = options["dry_run"]
        changed = 0
        scanned = 0
        sheets = 0

        for Model in (RateSheet, SystemRateSheet):
            for sheet in Model.objects.all().iterator():
                sheets += 1
                zones_by_id = {z["id"]: z for z in (sheet.zones or []) if isinstance(z, dict) and z.get("id")}
                origin = sheet.origin_countries or []
                for service in sheet.services.all():
                    scanned += 1
                    domicile, international = derive_destination_flags(service.zone_ids or [], zones_by_id, origin)
                    if (service.domicile, service.international) == (domicile, international):
                        continue
                    changed += 1
                    self.stdout.write(
                        f"  {Model.__name__} '{sheet.name}' / {service.service_code}: "
                        f"({service.domicile}, {service.international}) -> ({domicile}, {international})"
                    )
                    if not dry_run:
                        service.domicile = domicile
                        service.international = international
                        service.save(update_fields=["domicile", "international"])

        verb = "Would update" if dry_run else "Updated"
        self.stdout.write(
            self.style.SUCCESS(
                f"\n{verb} {changed} service level(s) across {sheets} rate sheet(s) ({scanned} scanned)."
            )
        )
