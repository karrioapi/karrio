"use client";

import React, { useRef, useState, useEffect, useMemo } from "react";
import { useVirtualizer } from "@tanstack/react-virtual";
import { PlusIcon, TrashIcon, Cross2Icon, Pencil1Icon } from "@radix-ui/react-icons";
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "@karrio/ui/components/ui/popover";
import {
  Tooltip,
  TooltipContent,
  TooltipProvider,
  TooltipTrigger,
} from "@karrio/ui/components/ui/tooltip";
import { AddWeightRangePopover } from "@karrio/ui/components/add-weight-range-popover";
import type {
  ServiceLevelWithZones,
  EmbeddedZone,
} from "@karrio/ui/components/rate-sheet-editor";
import {
  buildRateLookupMap,
  type WeightRange,
  type ServiceRate,
  type RateCellKey,
} from "@karrio/ui/components/weight-rate-grid";

// ─────────────────────────────────────────────────────
// Editable Cell
// ─────────────────────────────────────────────────────

const EditableCell = React.memo(
  ({
    value,
    onSave,
  }: {
    value: number | null | undefined;
    onSave: (value: string) => void;
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
      const trimmed = editValue.trim();
      const parsed = parseFloat(trimmed);
      if (trimmed === "" || isNaN(parsed)) {
        // Revert to previous value on empty/invalid input
        setEditValue(localValue);
      } else if (editValue !== localValue) {
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
          className="w-full h-full p-0 border-none outline-none ring-0 text-center text-sm text-foreground relative z-20 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-primary bg-background"
        />
      );
    }

    return (
      <div
        className="w-full h-full px-2 py-2 text-center text-sm text-muted-foreground cursor-pointer hover:bg-accent flex items-center justify-center"
        onClick={() => setIsEditing(true)}
        title="Click to edit"
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
// Props
// ─────────────────────────────────────────────────────

interface ServiceRateDetailViewProps {
  service: ServiceLevelWithZones;
  sharedZones: EmbeddedZone[];
  serviceRates: ServiceRate[];
  weightRanges: WeightRange[];
  serviceFilteredWeightRanges?: WeightRange[];
  weightUnit: string;
  onCellEdit: (
    serviceId: string,
    zoneId: string,
    minWeight: number,
    maxWeight: number,
    newRate: number
  ) => void;
  onDeleteRate?: (
    serviceId: string,
    zoneId: string,
    minWeight: number,
    maxWeight: number
  ) => void;
  onAddWeightRange?: () => void;
  onRemoveWeightRange?: (minWeight: number, maxWeight: number) => void;
  onEditWeightRange?: (range: WeightRange) => void;
  onEditZone?: (zone: EmbeddedZone) => void;
  onDeleteZone?: (zoneLabel: string) => void;
  onAssignZoneToService?: (serviceId: string, zoneId: string) => void;
  onCreateNewZone?: (serviceId: string) => void;
  onRemoveZoneFromService?: (serviceId: string, zoneId: string) => void;
  missingRanges?: WeightRange[];
  onAddMissingRange?: (minWeight: number, maxWeight: number) => void;
  weightRangePresets?: { min_weight: number; max_weight: number }[];
  onAddFromPreset?: (minWeight: number, maxWeight: number) => void;
}

export function ServiceRateDetailView({
  service,
  sharedZones,
  serviceRates,
  weightRanges,
  serviceFilteredWeightRanges,
  weightUnit,
  onCellEdit,
  onDeleteRate,
  onAddWeightRange,
  onRemoveWeightRange,
  onEditWeightRange,
  onEditZone,
  onDeleteZone,
  onAssignZoneToService,
  onCreateNewZone,
  onRemoveZoneFromService,
  missingRanges,
  onAddMissingRange,
  weightRangePresets,
  onAddFromPreset,
}: ServiceRateDetailViewProps) {
  const parentRef = useRef<HTMLDivElement>(null);
  const [zonePopoverOpen, setZonePopoverOpen] = useState(false);

  const serviceZoneIds = service.zone_ids || [];
  const assignedZones = useMemo(
    () => sharedZones.filter((z) => serviceZoneIds.includes(z.id)),
    [sharedZones, serviceZoneIds]
  );

  const unassignedZones = useMemo(
    () => sharedZones.filter((z) => !serviceZoneIds.includes(z.id)),
    [sharedZones, serviceZoneIds]
  );

  const rateLookup = useMemo(
    () => buildRateLookupMap(serviceRates),
    [serviceRates]
  );

  // Use service-filtered weight ranges if provided, else global
  const effectiveWeightRanges = serviceFilteredWeightRanges ?? weightRanges;

  const rows = useMemo(() => {
    if (effectiveWeightRanges.length === 0) {
      return [{ min_weight: 0, max_weight: 0 }];
    }
    return effectiveWeightRanges;
  }, [effectiveWeightRanges]);

  const rowVirtualizer = useVirtualizer({
    count: rows.length,
    getScrollElement: () => parentRef.current,
    estimateSize: () => 40,
    overscan: 10,
  });

  const hasAddZone = !!(onAssignZoneToService || onCreateNewZone);
  const weightColWidth = 200;
  const zoneColWidth = 140;
  const addZoneColWidth = 40;
  const tableWidth =
    weightColWidth +
    assignedZones.length * zoneColWidth +
    (hasAddZone ? addZoneColWidth : 0);

  // Build zone tooltip text
  const buildZoneTooltip = (zone: EmbeddedZone): string => {
    const parts: string[] = [];
    if (zone.country_codes?.length) {
      parts.push(`Countries: ${zone.country_codes.join(", ")}`);
    }
    if (zone.transit_days != null) {
      parts.push(`Transit: ${zone.transit_days} days`);
    }
    return parts.length > 0 ? parts.join("\n") : zone.label || "";
  };

  // Build weight range tooltip text
  const buildWeightTooltip = (wr: WeightRange): string => {
    const serviceRatesForRange = serviceRates.filter(
      (sr) =>
        sr.service_id === service.id &&
        sr.min_weight === wr.min_weight &&
        sr.max_weight === wr.max_weight &&
        sr.rate != null &&
        sr.rate > 0
    );
    const count = serviceRatesForRange.length;
    if (count === 0) return "No rates set";
    const avg =
      serviceRatesForRange.reduce((sum, r) => sum + (r.rate ?? 0), 0) / count;
    return `${count} rate${count !== 1 ? "s" : ""}, avg ${avg.toFixed(2)}`;
  };

  if (assignedZones.length === 0) {
    return (
      <div className="flex-1 flex items-center justify-center text-muted-foreground bg-muted/50 rounded border-2 border-dashed">
        <div className="text-center p-8">
          <p className="text-sm">No zones assigned to this service</p>
          {hasAddZone && (
            <button
              onClick={() =>
                onCreateNewZone
                  ? onCreateNewZone(service.id)
                  : onAssignZoneToService?.(service.id, "")
              }
              className="mt-2 text-xs text-primary hover:underline"
            >
              + Add zone
            </button>
          )}
        </div>
      </div>
    );
  }

  const formatWeightLabel = (wr: WeightRange, isFlat: boolean): string => {
    if (isFlat) return "Flat rate";
    if (wr.min_weight === 0) return `Up to ${wr.max_weight} ${weightUnit}`;
    return `${wr.min_weight} \u2013 ${wr.max_weight} ${weightUnit}`;
  };

  return (
    <TooltipProvider delayDuration={300}>
      <div className="h-full flex flex-col">
        <div className="flex-1 flex flex-col border border-border rounded-md bg-background overflow-hidden">
          <div ref={parentRef} className="flex-1 overflow-auto">
            <div style={{ minWidth: `${tableWidth}px` }}>
              {/* Header */}
              <div className="flex border-b border-border bg-muted font-medium text-sm text-foreground sticky top-0 z-30 shadow-sm">
                <div
                  className="p-3 border-r border-border flex-shrink-0 bg-muted sticky left-0 z-40 shadow-[2px_0_5px_-2px_rgba(0,0,0,0.1)]"
                  style={{ width: `${weightColWidth}px` }}
                >
                  Weight ({weightUnit})
                </div>
                {assignedZones.map((zone, index) => (
                  <div
                    key={zone.id || index}
                    className="p-3 border-r border-border flex-shrink-0 bg-muted group/zone"
                    style={{ width: `${zoneColWidth}px` }}
                  >
                    <div className="flex items-center justify-center gap-0.5">
                      <Tooltip>
                        <TooltipTrigger asChild>
                          <span
                            className="truncate text-center flex-1 min-w-0 cursor-default"
                          >
                            {zone.label || `Zone ${index + 1}`}
                          </span>
                        </TooltipTrigger>
                        <TooltipContent side="bottom" className="max-w-xs text-xs whitespace-pre-line">
                          {buildZoneTooltip(zone)}
                        </TooltipContent>
                      </Tooltip>
                      <div className="flex items-center gap-0 opacity-0 group-hover/zone:opacity-100 transition-all flex-shrink-0 bg-muted">
                        {onEditZone && (
                          <button
                            onClick={() => onEditZone(zone)}
                            className="p-0.5 rounded-sm text-muted-foreground hover:text-primary hover:bg-accent/50"
                            title={`Edit ${zone.label || "zone"}`}
                          >
                            <Pencil1Icon className="h-3 w-3" />
                          </button>
                        )}
                        {onDeleteZone && (
                          <button
                            onClick={() => onDeleteZone(zone.label)}
                            className="p-0.5 rounded-sm text-muted-foreground hover:text-destructive hover:bg-destructive/10"
                            title={`Delete ${zone.label || "zone"}`}
                          >
                            <TrashIcon className="h-3 w-3" />
                          </button>
                        )}
                        {onRemoveZoneFromService && (
                          <button
                            onClick={() =>
                              onRemoveZoneFromService(service.id, zone.id)
                            }
                            className="p-0.5 rounded-sm text-muted-foreground hover:text-destructive hover:bg-destructive/10"
                            title={`Remove ${zone.label || "zone"} from this service`}
                          >
                            <Cross2Icon className="h-3 w-3" />
                          </button>
                        )}
                      </div>
                    </div>
                  </div>
                ))}
                {hasAddZone && (
                  <div
                    className="flex-shrink-0 bg-muted flex items-center justify-center border-r border-border"
                    style={{ width: `${addZoneColWidth}px` }}
                  >
                    <Popover
                      open={zonePopoverOpen}
                      onOpenChange={setZonePopoverOpen}
                    >
                      <PopoverTrigger asChild>
                        <button
                          className="p-1 text-muted-foreground hover:text-primary transition-colors"
                          title="Add zone to this service"
                        >
                          <PlusIcon className="h-3.5 w-3.5" />
                        </button>
                      </PopoverTrigger>
                      <PopoverContent
                        align="start"
                        className="w-56 p-2"
                        sideOffset={8}
                      >
                        <div className="space-y-1">
                          <p className="text-xs font-medium text-muted-foreground px-2 py-1">
                            Add zone
                          </p>

                          {unassignedZones.length > 0 && (
                            <>
                              <div className="max-h-48 overflow-y-auto space-y-0.5">
                                {unassignedZones.map((zone) => (
                                  <button
                                    key={zone.id}
                                    onClick={() => {
                                      onAssignZoneToService?.(
                                        service.id,
                                        zone.id
                                      );
                                      setZonePopoverOpen(false);
                                    }}
                                    className="w-full text-left px-2 py-1.5 text-sm rounded-md hover:bg-accent transition-colors truncate"
                                    title={zone.label}
                                  >
                                    {zone.label || zone.id}
                                  </button>
                                ))}
                              </div>
                              <div className="border-t border-border my-1" />
                            </>
                          )}

                          {onCreateNewZone && (
                            <button
                              onClick={() => {
                                onCreateNewZone(service.id);
                                setZonePopoverOpen(false);
                              }}
                              className="w-full text-left px-2 py-1.5 text-sm rounded-md hover:bg-accent transition-colors flex items-center gap-1.5 text-primary font-medium"
                            >
                              <PlusIcon className="h-3.5 w-3.5" />
                              Create new zone
                            </button>
                          )}
                        </div>
                      </PopoverContent>
                    </Popover>
                  </div>
                )}
              </div>

              {/* Rows */}
              <div
                style={{
                  height: `${rowVirtualizer.getTotalSize()}px`,
                  position: "relative",
                }}
              >
                {rowVirtualizer.getVirtualItems().map((virtualRow) => {
                  const wr = rows[virtualRow.index];
                  const isFlat = wr.min_weight === 0 && wr.max_weight === 0;

                  return (
                    <div
                      key={virtualRow.key}
                      className="absolute top-0 left-0 w-full flex border-b border-border group hover:bg-muted/50 transition-colors"
                      style={{
                        height: `${virtualRow.size}px`,
                        transform: `translateY(${virtualRow.start}px)`,
                      }}
                    >
                      <div
                        className="px-3 py-2 border-r border-border flex-shrink-0 bg-background sticky left-0 z-20 flex items-center justify-between shadow-[2px_0_5px_-2px_rgba(0,0,0,0.1)]"
                        style={{ width: `${weightColWidth}px` }}
                      >
                        <Tooltip>
                          <TooltipTrigger asChild>
                            <span className="text-sm text-foreground cursor-default">
                              {formatWeightLabel(wr, isFlat)}
                            </span>
                          </TooltipTrigger>
                          {!isFlat && (
                            <TooltipContent side="right" className="text-xs">
                              {buildWeightTooltip(wr)}
                            </TooltipContent>
                          )}
                        </Tooltip>
                        <div className="flex items-center gap-0 opacity-0 group-hover:opacity-100 transition-opacity">
                          {onEditWeightRange && !isFlat && (
                            <button
                              onClick={() => onEditWeightRange(wr)}
                              className="p-0.5 text-muted-foreground hover:text-primary"
                              title="Edit weight range"
                            >
                              <Pencil1Icon className="h-3 w-3" />
                            </button>
                          )}
                          {onRemoveWeightRange && !isFlat && (
                            <button
                              onClick={() =>
                                onRemoveWeightRange(wr.min_weight, wr.max_weight)
                              }
                              className="p-0.5 text-muted-foreground hover:text-destructive"
                              title="Remove weight range"
                            >
                              <TrashIcon className="h-3 w-3" />
                            </button>
                          )}
                        </div>
                      </div>

                      {assignedZones.map((zone) => {
                        const key: RateCellKey = `${service.id}:${zone.id}:${wr.min_weight}:${wr.max_weight}`;
                        const cell = rateLookup.get(key);
                        const hasValue = cell?.rate != null && cell.rate > 0;

                        return (
                          <div
                            key={zone.id}
                            className="border-r border-border flex-shrink-0 relative group/cell"
                            style={{ width: `${zoneColWidth}px` }}
                          >
                            <EditableCell
                              value={cell?.rate ?? null}
                              onSave={(val) => {
                                const newRate = parseFloat(val);
                                if (!isNaN(newRate)) {
                                  onCellEdit(
                                    service.id,
                                    zone.id,
                                    wr.min_weight,
                                    wr.max_weight,
                                    newRate
                                  );
                                }
                              }}
                            />
                            {onDeleteRate && hasValue && (
                              <button
                                onClick={(e) => {
                                  e.stopPropagation();
                                  onDeleteRate(
                                    service.id,
                                    zone.id,
                                    wr.min_weight,
                                    wr.max_weight
                                  );
                                }}
                                className="absolute inset-y-0 right-px my-auto h-4 w-4 flex items-center justify-center opacity-0 group-hover/cell:opacity-100 text-muted-foreground hover:text-destructive transition-opacity z-10"
                                title="Delete rate"
                              >
                                <Cross2Icon className="h-2.5 w-2.5" />
                              </button>
                            )}
                          </div>
                        );
                      })}

                      {/* Spacer for add-zone column */}
                      {hasAddZone && (
                        <div
                          className="flex-shrink-0"
                          style={{ width: `${addZoneColWidth}px` }}
                        />
                      )}
                    </div>
                  );
                })}
              </div>
            </div>
          </div>

        </div>

        {/* Add Weight Range — below the grid, left-aligned under weight column */}
        {onAddWeightRange && (
          <div className="border-t border-border px-3 py-2" style={{ maxWidth: `${weightColWidth}px` }}>
            <AddWeightRangePopover
              onAddWeightRange={onAddWeightRange}
              weightUnit={weightUnit}
              weightRangePresets={weightRangePresets}
              onAddFromPreset={onAddFromPreset}
              missingRanges={missingRanges}
              onAddMissingRange={onAddMissingRange}
            />
          </div>
        )}
      </div>
    </TooltipProvider>
  );
}

export default ServiceRateDetailView;
