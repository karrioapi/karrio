"use client";

import React, { useMemo, useRef, useDeferredValue, useCallback } from "react";
import {
  Sheet,
  SheetContent,
  SheetHeader,
  SheetTitle,
} from "@karrio/ui/components/ui/sheet";
import { Cross2Icon } from "@radix-ui/react-icons";
import { useVirtualizer } from "@tanstack/react-virtual";
import { cn } from "@karrio/ui/lib/utils";
import { Loader2 } from "lucide-react";
import type {
  ServiceLevelWithZones,
  EmbeddedZone,
  SharedSurcharge,
} from "@karrio/ui/components/rate-sheet-editor";
import type { ServiceRate, WeightRange } from "@karrio/ui/components/weight-rate-grid";

// ─────────────────────────────────────────────────────
// Types
// ─────────────────────────────────────────────────────

interface FlatRow {
  type: string;
  fromCountry: string;
  zone: string;
  carrierCode: string;
  serviceCode: string;
  serviceName: string;
  minWeight: number;
  maxWeight: number;
  maxLength: number | null;
  maxWidth: number | null;
  maxHeight: number | null;
  rate: number | null;
  currency: string;
  weightUnit: string;
  surcharges: Record<string, number>;
}

interface ColumnDef {
  key: string;
  label: string;
  width: number;
}

interface RateSheetCsvPreviewProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  name: string;
  carrierName: string;
  originCountries: string[];
  services: ServiceLevelWithZones[];
  sharedZones: EmbeddedZone[];
  serviceRates: ServiceRate[];
  weightRanges: WeightRange[];
  surcharges: SharedSurcharge[];
  weightUnit: string;
}

// ─────────────────────────────────────────────────────
// Columns definition
// ─────────────────────────────────────────────────────

const FIXED_COLUMNS: ColumnDef[] = [
  { key: "type", label: "Type", width: 100 },
  { key: "fromCountry", label: "From", width: 60 },
  { key: "zone", label: "Zone", width: 120 },
  { key: "carrierCode", label: "Carrier", width: 100 },
  { key: "serviceCode", label: "Service Code", width: 140 },
  { key: "serviceName", label: "Service Name", width: 200 },
  { key: "minWeight", label: "Min Weight", width: 90 },
  { key: "maxWeight", label: "Max Weight", width: 90 },
  { key: "maxLength", label: "Max Length", width: 90 },
  { key: "maxWidth", label: "Max Width", width: 90 },
  { key: "maxHeight", label: "Max Height", width: 90 },
  { key: "rate", label: "Base Rate", width: 90 },
  { key: "currency", label: "Currency", width: 70 },
];

const EMPTY_ROWS: FlatRow[] = [];

// ─────────────────────────────────────────────────────
// Pure helpers (stable references — no re-creation)
// ─────────────────────────────────────────────────────

function formatCell(row: FlatRow, colKey: string): string {
  switch (colKey) {
    case "type":
      return row.type;
    case "fromCountry":
      return row.fromCountry;
    case "zone":
      return row.zone;
    case "carrierCode":
      return row.carrierCode;
    case "serviceCode":
      return row.serviceCode;
    case "serviceName":
      return row.serviceName;
    case "minWeight":
      return row.minWeight.toString();
    case "maxWeight":
      return row.maxWeight.toString();
    case "maxLength":
      return row.maxLength?.toString() || "";
    case "maxWidth":
      return row.maxWidth?.toString() || "";
    case "maxHeight":
      return row.maxHeight?.toString() || "";
    case "rate":
      return row.rate != null ? row.rate.toFixed(2) : "";
    case "currency":
      return row.currency;
    default:
      // Surcharge column
      return row.surcharges[colKey] != null
        ? row.surcharges[colKey].toFixed(2)
        : "";
  }
}

// ─────────────────────────────────────────────────────
// Memoized virtual row component
// ─────────────────────────────────────────────────────

interface VirtualRowProps {
  row: FlatRow;
  rowIndex: number;
  columns: ColumnDef[];
  height: number;
  start: number;
}

const VirtualRow = React.memo(function VirtualRow({
  row,
  rowIndex,
  columns,
  height,
  start,
}: VirtualRowProps) {
  return (
    <div
      className={cn(
        "absolute top-0 left-0 w-full flex border-b border-border text-xs",
        rowIndex % 2 === 0 ? "bg-background" : "bg-muted/30"
      )}
      style={{
        height: `${height}px`,
        transform: `translateY(${start}px)`,
      }}
    >
      {/* Row number */}
      <div className="w-10 px-2 py-1.5 border-r border-border flex-shrink-0 bg-background text-center text-muted-foreground sticky left-0 z-10">
        {rowIndex + 1}
      </div>

      {columns.map((col) => {
        const value = formatCell(row, col.key);
        return (
          <div
            key={col.key}
            className="px-2 py-1.5 border-r border-border flex-shrink-0 truncate text-foreground"
            style={{ width: `${col.width}px` }}
            title={value}
          >
            {value}
          </div>
        );
      })}
    </div>
  );
});

// ─────────────────────────────────────────────────────
// Component
// ─────────────────────────────────────────────────────

export function RateSheetCsvPreview({
  open,
  onOpenChange,
  name,
  carrierName,
  originCountries,
  services,
  sharedZones,
  serviceRates,
  weightRanges,
  surcharges,
  weightUnit,
}: RateSheetCsvPreviewProps) {
  const parentRef = useRef<HTMLDivElement>(null);

  // ── Lazy guard: skip all computation when panel is closed ──
  // Build a lookup for service rates
  const rateLookup = useMemo(() => {
    if (!open) return new Map<string, number>();
    const map = new Map<string, number>();
    for (const sr of serviceRates) {
      const key = `${sr.service_id}:${sr.zone_id}:${sr.min_weight ?? 0}:${sr.max_weight ?? 0}`;
      map.set(key, sr.rate);
    }
    return map;
  }, [open, serviceRates]);

  // Derive surcharge column names
  const surchargeColumns = useMemo(
    () =>
      open
        ? surcharges
            .filter((s) => s.name)
            .map((s) => ({ key: s.id, label: s.name, width: 100 }))
        : [],
    [open, surcharges]
  );

  // Pre-build surcharge lookup: surchargeId → amount (O(1) per row instead of O(n))
  const surchargeAmountMap = useMemo(() => {
    if (!open) return new Map<string, number>();
    const map = new Map<string, number>();
    for (const s of surcharges) {
      map.set(s.id, s.amount);
    }
    return map;
  }, [open, surcharges]);

  // Build flat rows: service × zone × weight_range
  const rows = useMemo(() => {
    if (!open) return EMPTY_ROWS;

    const result: FlatRow[] = [];
    const fromCountry = originCountries.join(", ") || "—";

    const effectiveRanges: WeightRange[] =
      weightRanges.length > 0
        ? weightRanges
        : [{ min_weight: 0, max_weight: 0 }];

    for (const service of services) {
      const assignedZoneIds = service.zone_ids || [];
      const assignedZones = assignedZoneIds
        .map((zid) => sharedZones.find((z) => z.id === zid))
        .filter(Boolean) as EmbeddedZone[];

      // Pre-build surcharge amounts for this service (Set for O(1) membership check)
      const linkedIds = new Set(service.surcharge_ids || []);
      const surchAmounts: Record<string, number> = {};
      for (const [sid, amount] of surchargeAmountMap) {
        if (linkedIds.has(sid)) {
          surchAmounts[sid] = amount;
        }
      }

      const isReturn =
        (service.features || []).includes("returns") ||
        /\breturn/i.test(service.service_name || "") ||
        /\breturn/i.test(service.service_code || "");
      const serviceType = isReturn ? "RETURN" : "SHIPPING";

      // Skip services with no zones assigned (no rates to show)
      if (assignedZones.length === 0) continue;

      for (const zone of assignedZones) {
        for (const wr of effectiveRanges) {
          const rateKey = `${service.id}:${zone.id}:${wr.min_weight}:${wr.max_weight}`;
          const rate = rateLookup.get(rateKey) ?? null;

          result.push({
            type: serviceType,
            fromCountry,
            zone: zone.label || "—",
            carrierCode: carrierName,
            serviceCode: service.service_code,
            serviceName: service.service_name,
            minWeight: wr.min_weight,
            maxWeight: wr.max_weight,
            maxLength: service.max_length ?? null,
            maxWidth: service.max_width ?? null,
            maxHeight: service.max_height ?? null,
            rate,
            currency: service.currency || "USD",
            weightUnit: service.weight_unit || weightUnit,
            surcharges: surchAmounts,
          });
        }
      }
    }

    return result;
  }, [
    open,
    services,
    sharedZones,
    weightRanges,
    surchargeAmountMap,
    carrierName,
    originCountries,
    weightUnit,
    rateLookup,
  ]);

  // ── Deferred value: lets React prioritise the Sheet animation over row rendering ──
  const deferredRows = useDeferredValue(rows);
  const isStale = deferredRows !== rows;

  const allColumns = useMemo(
    () => [...FIXED_COLUMNS, ...surchargeColumns],
    [surchargeColumns]
  );
  const totalWidth = useMemo(
    () => allColumns.reduce((sum, col) => sum + col.width, 0),
    [allColumns]
  );

  const rowVirtualizer = useVirtualizer({
    count: deferredRows.length,
    getScrollElement: () => parentRef.current,
    estimateSize: () => 32,
    overscan: 5,
  });

  const handleClose = useCallback(
    () => onOpenChange(false),
    [onOpenChange]
  );

  return (
    <Sheet open={open} onOpenChange={onOpenChange}>
      <SheetContent
        side="right"
        className="w-full sm:max-w-full p-0"
        hideCloseButton
      >
        <SheetHeader className="px-4 sm:px-6 py-4 border-b border-border bg-background">
          <div className="flex items-center justify-between gap-3">
            <SheetTitle className="text-lg font-semibold flex-1">
              {name || "Rate Sheet"} — Preview
            </SheetTitle>
            <div className="flex items-center gap-2 text-sm text-muted-foreground">
              <span>{rows.length} rows</span>
              <span className="text-border">|</span>
              <span>{allColumns.length} columns</span>
            </div>
            <button
              onClick={handleClose}
              className="p-2 rounded-md text-muted-foreground hover:text-foreground hover:bg-accent transition-colors"
              aria-label="Close preview"
            >
              <Cross2Icon className="h-5 w-5" />
            </button>
          </div>
        </SheetHeader>

        <div className="flex-1 h-[calc(100vh-73px)] overflow-hidden">
          {rows.length === 0 ? (
            <div className="flex items-center justify-center h-full text-muted-foreground">
              <div className="text-center p-8">
                <p className="text-sm">No data to preview</p>
                <p className="text-xs mt-1">
                  Add services and configure rates to see the preview
                </p>
              </div>
            </div>
          ) : (
            <div className="relative h-full">
              {/* Loading overlay while deferred rows catch up */}
              {isStale && (
                <div className="absolute inset-0 z-30 flex items-center justify-center bg-background/60">
                  <div className="flex items-center gap-2 text-sm text-muted-foreground">
                    <Loader2 className="h-4 w-4 animate-spin" />
                    <span>Loading preview...</span>
                  </div>
                </div>
              )}

              <div
                ref={parentRef}
                className={cn(
                  "h-full overflow-auto transition-opacity duration-150",
                  isStale && "opacity-60"
                )}
              >
                <div style={{ minWidth: `${totalWidth}px` }}>
                  {/* Header */}
                  <div className="flex border-b border-border bg-muted font-medium text-xs text-foreground sticky top-0 z-10">
                    <div className="w-10 px-2 py-2 border-r border-border flex-shrink-0 bg-muted text-center text-muted-foreground sticky left-0 z-20">
                      #
                    </div>
                    {allColumns.map((col) => (
                      <div
                        key={col.key}
                        className="px-2 py-2 border-r border-border flex-shrink-0 bg-muted truncate"
                        style={{ width: `${col.width}px` }}
                        title={col.label}
                      >
                        {col.label}
                      </div>
                    ))}
                  </div>

                  {/* Virtualized rows */}
                  <div
                    style={{
                      height: `${rowVirtualizer.getTotalSize()}px`,
                      position: "relative",
                    }}
                  >
                    {rowVirtualizer.getVirtualItems().map((virtualRow) => (
                      <VirtualRow
                        key={virtualRow.key}
                        row={deferredRows[virtualRow.index]}
                        rowIndex={virtualRow.index}
                        columns={allColumns}
                        height={virtualRow.size}
                        start={virtualRow.start}
                      />
                    ))}
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>
      </SheetContent>
    </Sheet>
  );
}

export default RateSheetCsvPreview;
