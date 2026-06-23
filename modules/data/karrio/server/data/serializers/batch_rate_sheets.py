"""
BatchOperation handler for rate_sheet imports.

Handles:
  - New flat xlsx import (single service_rates sheet) — primary path
  - Legacy multi-sheet xlsx import (5-6 sheets) — fallback
  - Flat CSV import (carrier_name column present)
  - Legacy CSV service_rates-only import
  - dry_run=true → validate + diff, no writes
  - Sync upsert (no background queue needed for rate sheets — data is small)
"""

import karrio.server.data.resources.rate_sheets as rs_resource


def process_rate_sheet_import(
    data_file,
    context,
    dry_run: bool = False,
    rate_sheet_id: str = None,
) -> dict:
    """
    Parse and validate a rate sheet file. If dry_run=False, upsert to DB.

    Returns:
        {
            "dry_run": bool,
            "errors": [...],          # only on validation failure
            "diff": {...},            # only on dry_run=True success
            "rate_sheet_id": str,     # only on successful write
            "created": bool,          # only on successful write
        }
    """
    from karrio.server.providers.models import RateSheet

    raw = data_file.read() if hasattr(data_file, "read") else data_file
    filename = getattr(data_file, "name", "") or ""

    file_fmt = rs_resource.detect_format(raw, filename)

    # ── CSV ──────────────────────────────────────────────────────────────────
    if file_fmt == "csv":
        rows = rs_resource._csv_rows(raw)

        # Detect flat vs legacy CSV by presence of carrier_name column
        if rows and "carrier_name" in (rows[0] or {}):
            # Flat CSV path
            errors = rs_resource.validate_flat_data(rows)
            if errors:
                return {"dry_run": dry_run, "errors": errors}

            carrier_inputs = rs_resource.build_rate_sheet_input_from_flat(rows)
            if not carrier_inputs:
                return {
                    "dry_run": dry_run,
                    "errors": [
                        {"sheet": "service_rates", "row": 0, "field": "", "message": "No carrier data found in CSV"}
                    ],
                }
            carrier_name = next(iter(carrier_inputs))
            payload = rs_resource.flat_carrier_to_upsert_payload(carrier_inputs[carrier_name])
        else:
            # Legacy CSV path — requires an existing rate sheet context
            parsed = rs_resource.parse_csv(raw, context=context, rate_sheet_id=rate_sheet_id)
            if rate_sheet_id:
                existing = (
                    RateSheet.access_by(context).filter(slug=rate_sheet_id).first()
                    or RateSheet.access_by(context).filter(id=rate_sheet_id).first()
                )
                if existing:
                    parsed["rate_sheet"] = [
                        {
                            "name": existing.name,
                            "carrier_name": existing.carrier_name,
                            "slug": existing.slug,
                        }
                    ]
                    parsed["zones"] = [
                        {"zone_id": z.get("id"), "zone_label": z.get("label"), **z} for z in (existing.zones or [])
                    ]
                    parsed["services"] = []
                    parsed["surcharges"] = [
                        {"surcharge_id": s.get("id"), "surcharge_name": s.get("name"), **s}
                        for s in (existing.surcharges or [])
                    ]

            errors = rs_resource.validate_workbook(parsed)
            if errors:
                return {"dry_run": dry_run, "errors": errors}
            payload = rs_resource.build_upsert_payload(parsed)

    # ── XLSX / XLS ────────────────────────────────────────────────────────────
    else:
        wb_fmt = rs_resource.detect_workbook_format(raw)

        if wb_fmt == "flat":
            # ── New flat format ───────────────────────────────────────────────
            rows = rs_resource.parse_flat_workbook(raw)
            errors = rs_resource.validate_flat_data(rows)
            if errors:
                return {"dry_run": dry_run, "errors": errors}

            carrier_inputs = rs_resource.build_rate_sheet_input_from_flat(rows)
            if not carrier_inputs:
                return {
                    "dry_run": dry_run,
                    "errors": [
                        {
                            "sheet": "service_rates",
                            "row": 0,
                            "field": "",
                            "message": "No carrier data found in workbook",
                        }
                    ],
                }
            # Take the first carrier (most files contain a single carrier)
            carrier_name = next(iter(carrier_inputs))
            payload = rs_resource.flat_carrier_to_upsert_payload(carrier_inputs[carrier_name])

        else:
            # ── Legacy multi-sheet format (fallback) ──────────────────────────
            parsed = rs_resource.parse_xlsx(raw)
            errors = rs_resource.validate_workbook(parsed)
            if errors:
                return {"dry_run": dry_run, "errors": errors}
            payload = rs_resource.build_upsert_payload(parsed)

    # ── Dry run: diff only, no writes ─────────────────────────────────────────
    if dry_run:
        slug = payload["rate_sheet"].get("slug")
        existing_sheet = None
        if slug:
            existing_sheet = RateSheet.access_by(context).filter(slug=slug).first()
        diff = rs_resource.compute_diff(existing_sheet, payload)
        return {
            "dry_run": True,
            "errors": [],
            "diff": diff,
            "rate_sheet": payload["rate_sheet"],
        }

    # ── Live upsert ───────────────────────────────────────────────────────────
    sheet, created = rs_resource.upsert_rate_sheet(payload, context)
    return {
        "dry_run": False,
        "errors": [],
        "rate_sheet_id": sheet.id,
        "created": created,
    }
