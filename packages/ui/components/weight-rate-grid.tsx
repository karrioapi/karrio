"use client";

import React, { useRef, useState, useEffect, useMemo, useCallback } from "react";
import { useVirtualizer } from "@tanstack/react-virtual";
import { PlusIcon, TrashIcon, ChevronRightIcon } from "@radix-ui/react-icons";
import { Button } from "@karrio/ui/components/ui/button";
import { cn } from "@karrio/ui/lib/utils";
import type {
  ServiceLevelWithZones,
  EmbeddedZone,
} from "@karrio/ui/components/rate-sheet-editor";

// ─────────────────────────────────────────────────────
// Types
// ─────────────────────────────────────────────────────

export interface WeightRange {
  min_weight: number;
  max_weight: number;
}

export interface ServiceRate {
  service_id: string;
  zone_id: string;
  rate: number;
  cost?: number | null;
  min_weight?: number | null;
  max_weight?: number | null;
  transit_days?: number | null;
  transit_time?: number | null;
}

export type RateCellKey = `${string}:${string}:${number}:${number}`;

export interface RateCellValue {
  rate: number;
  cost?: number | null;
}

export type RateLookupMap = Map<RateCellKey, RateCellValue>;

// ─────────────────────────────────────────────────────
// Helper: build lookup map for O(1) rate cell access
// ─────────────────────────────────────────────────────

export function buildRateLookupMap(
  serviceRates: ServiceRate[]
): RateLookupMap {
  const map: RateLookupMap = new Map();
  for (const sr of serviceRates) {
    const key: RateCellKey = `${sr.service_id}:${sr.zone_id}:${sr.min_weight ?? 0}:${sr.max_weight ?? 0}`;
    map.set(key, { rate: sr.rate, cost: sr.cost });
  }
  return map;
}

/** Derive unique weight ranges from service_rates, excluding (0,0) flat entries, sorted by max_weight. */
export function deriveWeightRanges(serviceRates: ServiceRate[]): WeightRange[] {
  const seen = new Set<string>();
  const ranges: WeightRange[] = [];
  for (const sr of serviceRates) {
    const min = sr.min_weight ?? 0;
    const max = sr.max_weight ?? 0;
    if (min === 0 && max === 0) continue;
    const key = `${min}:${max}`;
    if (!seen.has(key)) {
      seen.add(key);
      ranges.push({ min_weight: min, max_weight: max });
    }
  }
  return ranges.sort((a, b) => a.max_weight - b.max_weight);
}

// ─────────────────────────────────────────────────────
// Editable Cell
// ─────────────────────────────────────────────────────

const EditableCell = React.memo(
  ({
    value,
    onSave,
    disabled = false,
  }: {
    value: number | null | undefined;
    onSave: (value: string) => void;
    disabled?: boolean;
  }) => {
    const [isEditing, setIsEditing] = useState(false);
    const [editValue, setEditValue] = useState(value?.toString() || "");
    const [localValue, setLocalValue] = useState(value?.toString() || "");
    const inputRef = useRef<HTMLInputElement>(null);

    useEffect(() => {
      setLocalValue(value?.toString() || "");
      if (!isEditing) setEditValue(value?.toString() || "");
    }, [value, isEditing]);

    useEffect(() => {
      if (isEditing && inputRef.current) {
        inputRef.current.focus();
        inputRef.current.select();
      }
    }, [isEditing]);

    const handleSave = () => {
      if (editValue !== localValue) {
        onSave(editValue);
        setLocalValue(editValue);
      }
      setIsEditing(false);
    };

    const handleKeyDown = (e: React.KeyboardEvent) => {
      if (e.key === "Enter") handleSave();
      else if (e.key === "Escape") {
        setEditValue(localValue);
        setIsEditing(false);
      }
    };

    if (isEditing) {
      return (
        <input
          ref={inputRef}
          type="number"
          step="any"
          min="0"
          value={editValue}
          onChange={(e) => setEditValue(e.target.value)}
          onBlur={handleSave}
          onKeyDown={handleKeyDown}
          disabled={disabled}
          className="w-full h-full p-0 border-none outline-none ring-0 text-center text-sm text-foreground relative z-20 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-primary bg-background"
        />
      );
    }

    return (
      <div
        className={cn(
          "w-full h-full px-2 py-2 text-center text-sm text-muted-foreground cursor-pointer hover:bg-accent flex items-center justify-center",
          disabled && "cursor-not-allowed opacity-50"
        )}
        onClick={() => !disabled && setIsEditing(true)}
        title={disabled ? "Read only" : "Click to edit"}
      >
        <span>
          {localValue !== "" && !isNaN(Number(localValue))
            ? Number(localValue).toFixed(2)
            : "-"}
        </span>
      </div>
    );
  }
);

EditableCell.displayName = "EditableCell";

// ─────────────────────────────────────────────────────
// Grid
// ─────────────────────────────────────────────────────

interface WeightRateGridProps {
  services: ServiceLevelWithZones[];
  sharedZones: EmbeddedZone[];
  serviceRates: ServiceRate[];
  weightRanges: WeightRange[];
  weightUnit: string;
  onCellEdit: (
    serviceId: string,
    zoneId: string,
    minWeight: number,
    maxWeight: number,
    newRate: number
  ) => void;
  onAddWeightRange: () => void;
  onRemoveWeightRange: (minWeight: number, maxWeight: number) => void;
}

export function WeightRateGrid({
  services,
  sharedZones,
  serviceRates,
  weightRanges,
  weightUnit,
  onCellEdit,
  onAddWeightRange,
  onRemoveWeightRange,
}: WeightRateGridProps) {
  const parentRef = useRef<HTMLDivElement>(null);
  const [expandedRanges, setExpandedRanges] = useState<Set<string>>(new Set());

  const toggleRange = useCallback((wr: WeightRange) => {
    const key = `${wr.min_weight}:${wr.max_weight}`;
    setExpandedRanges(prev => {
      const next = new Set(prev);
      if (next.has(key)) next.delete(key);
      else next.add(key);
      return next;
    });
  }, []);

  const rateLookup = useMemo(
    () => buildRateLookupMap(serviceRates),
    [serviceRates]
  );

  const rows = useMemo(() => {
    const result: Array<{
      type: "weight-header" | "service-row";
      weightRange?: WeightRange;
      service?: ServiceLevelWithZones;
    }> = [];

    if (weightRanges.length === 0) {
      for (const service of services) {
        result.push({
          type: "service-row",
          service,
          weightRange: { min_weight: 0, max_weight: 0 },
        });
      }
    } else {
      for (const wr of weightRanges) {
        result.push({ type: "weight-header", weightRange: wr });
        const key = `${wr.min_weight}:${wr.max_weight}`;
        if (expandedRanges.has(key)) {
          for (const service of services) {
            result.push({ type: "service-row", service, weightRange: wr });
          }
        }
      }
    }

    return result;
  }, [services, weightRanges, expandedRanges]);

  const rowVirtualizer = useVirtualizer({
    count: rows.length,
    getScrollElement: () => parentRef.current,
    estimateSize: (index) => (rows[index].type === "weight-header" ? 36 : 40),
    overscan: 10,
  });

  const serviceColWidth = 192;
  const zoneColWidth = 112;
  const tableWidth = serviceColWidth + sharedZones.length * zoneColWidth;

  if (services.length === 0) {
    return (
      <div className="flex-1 flex items-center justify-center text-muted-foreground bg-muted/50 rounded border-2 border-dashed">
        <div className="text-center p-8">
          <p className="text-lg mb-2">No services configured</p>
          <p className="text-sm">
            Go to the Services tab to add services first
          </p>
        </div>
      </div>
    );
  }

  if (sharedZones.length === 0) {
    return (
      <div className="flex-1 flex items-center justify-center text-muted-foreground bg-muted/50 rounded border-2 border-dashed">
        <div className="text-center p-8">
          <p className="text-lg mb-2">No zones configured</p>
          <p className="text-sm">
            Go to the Zones tab to add zones first
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="h-full flex flex-col">
      <div className="flex-1 flex flex-col border border-border rounded-md bg-background overflow-hidden">
        <div ref={parentRef} className="flex-1 overflow-auto">
          <div style={{ minWidth: `${tableWidth}px` }}>
            {/* Header */}
            <div className="flex border-b border-border bg-muted font-medium text-sm text-foreground sticky top-0 z-30 shadow-sm">
              <div className="w-48 p-3 border-r border-border flex-shrink-0 bg-muted sticky left-0 z-40 shadow-[2px_0_5px_-2px_rgba(0,0,0,0.1)]">
                Service / Weight
              </div>
              {sharedZones.map((zone, index) => (
                <div
                  key={zone.id || zone.label || index}
                  className="w-28 p-3 border-r border-border flex-shrink-0 bg-muted"
                >
                  <span
                    className="truncate block text-center"
                    title={zone.label || `Zone ${index + 1}`}
                  >
                    {zone.label || `Zone ${index + 1}`}
                  </span>
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
              {rowVirtualizer.getVirtualItems().map((virtualRow) => {
                const row = rows[virtualRow.index];

                if (row.type === "weight-header") {
                  const wr = row.weightRange!;
                  return (
                    <div
                      key={virtualRow.key}
                      className="absolute top-0 left-0 w-full flex border-b border-border bg-muted/60"
                      style={{
                        height: `${virtualRow.size}px`,
                        transform: `translateY(${virtualRow.start}px)`,
                      }}
                    >
                      <div
                        className="flex items-center gap-2 px-3 py-1 sticky left-0 z-20 bg-muted/60 w-full cursor-pointer select-none"
                        onClick={() => toggleRange(wr)}
                      >
                        <ChevronRightIcon
                          className={cn(
                            "h-3.5 w-3.5 text-muted-foreground transition-transform",
                            expandedRanges.has(`${wr.min_weight}:${wr.max_weight}`) && "rotate-90"
                          )}
                        />
                        <span className="text-xs font-semibold text-foreground flex-1">
                          {wr.min_weight} – {wr.max_weight} {weightUnit}
                        </span>
                        <button
                          onClick={(e) => {
                            e.stopPropagation();
                            onRemoveWeightRange(wr.min_weight, wr.max_weight);
                          }}
                          className="p-0.5 text-muted-foreground hover:text-destructive hover:bg-destructive/10 rounded transition-colors"
                          title="Remove weight range"
                        >
                          <TrashIcon className="h-3 w-3" />
                        </button>
                      </div>
                    </div>
                  );
                }

                const service = row.service!;
                const wr = row.weightRange!;
                return (
                  <div
                    key={`${virtualRow.key}-${service.id}`}
                    className="absolute top-0 left-0 w-full flex border-b border-border hover:bg-muted/50 transition-colors"
                    style={{
                      height: `${virtualRow.size}px`,
                      transform: `translateY(${virtualRow.start}px)`,
                    }}
                  >
                    <div className="w-48 px-3 py-1 border-r border-border flex-shrink-0 bg-background sticky left-0 z-20 flex flex-col justify-center shadow-[2px_0_5px_-2px_rgba(0,0,0,0.1)]">
                      <span
                        className="text-sm font-medium text-foreground truncate"
                        title={service.service_name || ""}
                      >
                        {service.service_name || "Unnamed"}
                      </span>
                      {service.service_code && (
                        <span className="text-xs text-muted-foreground truncate">
                          {service.service_code}
                        </span>
                      )}
                    </div>

                    {sharedZones.map((zone) => {
                      const zoneId = zone.id;
                      const serviceZoneIds = service.zone_ids || [];
                      const isAssigned = serviceZoneIds.includes(zoneId);

                      const key: RateCellKey = `${service.id}:${zoneId}:${wr.min_weight}:${wr.max_weight}`;
                      const cell = rateLookup.get(key);

                      if (!isAssigned) {
                        return (
                          <div
                            key={zoneId}
                            className="w-28 border-r border-border flex-shrink-0 bg-muted/20"
                          >
                            <div className="w-full h-full flex items-center justify-center text-xs text-muted-foreground/40">
                              —
                            </div>
                          </div>
                        );
                      }

                      return (
                        <div
                          key={zoneId}
                          className="w-28 border-r border-border flex-shrink-0"
                        >
                          <EditableCell
                            value={cell?.rate ?? null}
                            onSave={(val) => {
                              const newRate = parseFloat(val);
                              if (!isNaN(newRate)) {
                                onCellEdit(
                                  service.id,
                                  zoneId,
                                  wr.min_weight,
                                  wr.max_weight,
                                  newRate
                                );
                              }
                            }}
                          />
                        </div>
                      );
                    })}
                  </div>
                );
              })}
            </div>
          </div>
        </div>
      </div>

      <div className="mt-4 flex justify-center">
        <Button onClick={onAddWeightRange} variant="outline">
          <PlusIcon className="h-4 w-4 mr-2" />
          Add Weight Range
        </Button>
      </div>
    </div>
  );
}

export default WeightRateGrid;
