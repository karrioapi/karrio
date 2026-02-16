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

export interface MarkupPreviewItem {
  id: string;
  name: string;
  amount: number;
  markup_type: string; // "AMOUNT" | "PERCENTAGE"
  active: boolean;
  meta?: {
    type?: string;
    plan?: string;
    show_in_preview?: boolean;
  };
}

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
  /** Progressive totals for each markup column */
  markups: Record<string, number>;
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
  markups?: MarkupPreviewItem[];
  isAdmin?: boolean;
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
    default: {
      // Surcharge column (prefixed with surch_)
      if (colKey.startsWith("surch_")) {
        const sid = colKey.slice(6);
        return row.surcharges[sid] != null
          ? row.surcharges[sid].toFixed(2)
          : "";
      }
      // Markup column (prefixed with mkp_) — progressive total
      if (colKey.startsWith("mkp_")) {
        const mid = colKey.slice(4);
        return row.markups[mid] != null
          ? row.markups[mid].toFixed(2)
          : "";
      }
      return "";
    }
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
  markups,
  isAdmin,
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

  // Pre-build surcharge lookup: surchargeId → { amount, surcharge_type }
  const surchargeDetailMap = useMemo(() => {
    if (!open) return new Map<string, { amount: number; surcharge_type: string }>();
    const map = new Map<string, { amount: number; surcharge_type: string }>();
    for (const s of surcharges) {
      map.set(s.id, { amount: s.amount, surcharge_type: s.surcharge_type || "fixed" });
    }
    return map;
  }, [open, surcharges]);

  // Filter markups to those with show_in_preview (admin only)
  const previewMarkups = useMemo(() => {
    if (!open || !isAdmin || !markups) return [];
    return markups.filter((m) => m.active && m.meta?.show_in_preview);
  }, [open, isAdmin, markups]);

  // Sort markups: non-brokerage first, then brokerage fees
  // Brokerage fees from different plans don't stack — each applies independently
  // on top of (base + surcharges + non-brokerage markups)
  const sortedPreviewMarkups = useMemo(() => {
    const nonBrokerage = previewMarkups.filter((m) => m.meta?.type !== "brokerage-fee");
    const brokerage = previewMarkups.filter((m) => m.meta?.type === "brokerage-fee");
    return [...nonBrokerage, ...brokerage];
  }, [previewMarkups]);

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

      // Pre-build linked surcharge IDs for this service
      const linkedIds = new Set(service.surcharge_ids || []);

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
          const baseRate = rate ?? 0;

          // Calculate surcharge amounts
          const surchAmounts: Record<string, number> = {};
          let surchargeTotal = 0;
          surchargeDetailMap.forEach((detail, sid) => {
            if (linkedIds.has(sid)) {
              const amt =
                detail.surcharge_type === "percentage"
                  ? baseRate * (detail.amount / 100)
                  : detail.amount;
              surchAmounts[sid] = amt;
              surchargeTotal += amt;
            }
          });

          // Calculate progressive markup totals
          // Non-brokerage markups accumulate progressively.
          // Brokerage fees each apply independently on top of
          // (base + surcharges + all non-brokerage markups) — they don't stack with each other.
          const mkpTotals: Record<string, number> = {};
          let nonBrokerageRunning = baseRate + surchargeTotal;

          // First pass: compute total non-brokerage contribution for brokerage base
          let nonBrokerageTotal = 0;
          for (const m of sortedPreviewMarkups) {
            if (m.meta?.type !== "brokerage-fee") {
              nonBrokerageTotal +=
                m.markup_type === "PERCENTAGE"
                  ? baseRate * (m.amount / 100)
                  : m.amount;
            }
          }
          const brokerageBase = baseRate + surchargeTotal + nonBrokerageTotal;

          // Second pass: compute progressive totals
          for (const m of sortedPreviewMarkups) {
            const contribution =
              m.markup_type === "PERCENTAGE"
                ? baseRate * (m.amount / 100)
                : m.amount;

            if (m.meta?.type === "brokerage-fee") {
              // Brokerage: base + surcharges + all non-brokerage + this brokerage only
              mkpTotals[m.id] = brokerageBase + contribution;
            } else {
              // Non-brokerage: progressive accumulation
              nonBrokerageRunning += contribution;
              mkpTotals[m.id] = nonBrokerageRunning;
            }
          }

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
            markups: mkpTotals,
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
    surchargeDetailMap,
    sortedPreviewMarkups,
    carrierName,
    originCountries,
    weightUnit,
    rateLookup,
  ]);

  // ── Deferred value: lets React prioritise the Sheet animation over row rendering ──
  const deferredRows = useDeferredValue(rows);
  const isStale = deferredRows !== rows;

  // Derive surcharge columns — omit columns where no row has a non-zero value
  const activeSurchargeColumns = useMemo(() => {
    if (!open) return [];
    return surcharges
      .filter((s) => s.name)
      .map((s) => ({
        key: `surch_${s.id}`,
        label: `${s.name} (${s.surcharge_type === "percentage" ? `${s.amount}%` : `$${s.amount.toFixed(2)}`})`,
        width: 110,
        id: s.id,
      }))
      .filter((col) => rows.some((row) => (row.surcharges[col.id] ?? 0) !== 0))
      .map(({ id: _, ...col }) => col);
  }, [open, surcharges, rows]);

  // Markup columns — show value in header, omit if contribution is 0 for all rows
  const activeMarkupColumns = useMemo(() => {
    return sortedPreviewMarkups
      .map((m) => {
        const valueLabel =
          m.markup_type === "PERCENTAGE"
            ? `${m.amount}%`
            : `$${m.amount.toFixed(2)}`;
        const planSuffix = m.meta?.plan ? ` - ${m.meta.plan}` : "";
        return {
          key: `mkp_${m.id}`,
          label: `${m.name}${planSuffix} (${valueLabel})`,
          width: 160,
          id: m.id,
          // Check if this markup has any meaningful contribution
          // A markup applies if its own contribution differs from the base (non-zero contribution)
          hasContribution: rows.some((row) => {
            const total = row.markups[m.id] ?? 0;
            // For brokerage: contribution = total - brokerageBase
            // For non-brokerage: any non-zero total means it contributes
            // Simplify: if the total differs from base+surcharges, the markup contributes
            const baseRate = row.rate ?? 0;
            let surchTotal = 0;
            for (const v of Object.values(row.surcharges)) surchTotal += v;
            return Math.abs(total - baseRate - surchTotal) > 0.001;
          }),
        };
      })
      .filter((col) => col.hasContribution)
      .map(({ id: _, hasContribution: __, ...col }) => col);
  }, [sortedPreviewMarkups, rows]);

  const allColumns = useMemo(
    () => [...FIXED_COLUMNS, ...activeSurchargeColumns, ...activeMarkupColumns],
    [activeSurchargeColumns, activeMarkupColumns]
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
