"use client";

import React from "react";
import { PlusIcon, TrashIcon, Pencil1Icon } from "@radix-ui/react-icons";
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "@karrio/ui/components/ui/popover";
import type { WeightRange, ServiceRate } from "@karrio/ui/components/weight-rate-grid";
import type {
  ServiceLevelWithZones,
  EmbeddedZone,
} from "@karrio/ui/components/rate-sheet-editor";

interface WeightRangePreset {
  min_weight: number;
  max_weight: number;
}

interface WeightRangesTabProps {
  weightRanges: WeightRange[];
  weightUnit: string;
  serviceRates: ServiceRate[];
  services: ServiceLevelWithZones[];
  sharedZones: EmbeddedZone[];
  onRemoveWeightRange: (minWeight: number, maxWeight: number) => void;
  onEditRate?: (serviceRate: ServiceRate) => void;
  weightRangePresets?: WeightRangePreset[];
  onAddFromPreset?: (minWeight: number, maxWeight: number) => void;
  onAddCustom?: () => void;
}

export function WeightRangesTab({
  weightRanges,
  weightUnit,
  serviceRates,
  services,
  sharedZones,
  onRemoveWeightRange,
  onEditRate,
  weightRangePresets,
  onAddFromPreset,
  onAddCustom,
}: WeightRangesTabProps) {
  const getServiceName = (serviceId: string) =>
    services.find((s) => s.id === serviceId)?.service_name || serviceId;

  const getZoneLabel = (zoneId: string) =>
    sharedZones.find((z) => z.id === zoneId)?.label || zoneId;

  const getRatesForRange = (range: WeightRange): ServiceRate[] =>
    serviceRates.filter(
      (sr) =>
        sr.min_weight === range.min_weight &&
        sr.max_weight === range.max_weight
    );

  const formatRangeLabel = (min: number, max: number) =>
    min === 0
      ? `Up to ${max} ${weightUnit}`
      : `${min} \u2013 ${max} ${weightUnit}`;

  const AddWeightRangePopover = ({ align = "end" }: { align?: "start" | "end" | "center" }) => (
    <Popover>
      <PopoverTrigger asChild>
        <button className="inline-flex items-center gap-2 px-4 py-2 text-sm font-medium text-primary-foreground bg-primary hover:bg-primary/90 rounded-md transition-colors">
          <PlusIcon className="h-4 w-4" />
          Add Weight Range
        </button>
      </PopoverTrigger>
      <PopoverContent align={align} className="w-56 p-2" sideOffset={8}>
        <div className="space-y-1">
          <p className="text-xs font-medium text-muted-foreground px-2 py-1">Add weight range</p>

          {weightRangePresets && weightRangePresets.length > 0 && onAddFromPreset && (
            <>
              <div className="max-h-48 overflow-y-auto space-y-0.5">
                {weightRangePresets.map((preset) => (
                  <button
                    key={`${preset.min_weight}-${preset.max_weight}`}
                    onClick={() => onAddFromPreset(preset.min_weight, preset.max_weight)}
                    className="w-full text-left px-2 py-1.5 text-sm rounded-md hover:bg-accent transition-colors truncate"
                    title={formatRangeLabel(preset.min_weight, preset.max_weight)}
                  >
                    {formatRangeLabel(preset.min_weight, preset.max_weight)}
                  </button>
                ))}
              </div>
              <div className="border-t border-border my-1" />
            </>
          )}

          {onAddCustom && (
            <button
              onClick={onAddCustom}
              className="w-full text-left px-2 py-1.5 text-sm rounded-md hover:bg-accent transition-colors flex items-center gap-1.5 text-primary font-medium"
            >
              <PlusIcon className="h-3.5 w-3.5" />
              Custom range
            </button>
          )}
        </div>
      </PopoverContent>
    </Popover>
  );

  if (weightRanges.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center h-full text-muted-foreground p-8">
        <p className="mb-4">No weight ranges configured yet.</p>
        <AddWeightRangePopover align="center" />
      </div>
    );
  }

  return (
    <div className="space-y-4 h-full overflow-y-auto pr-2">
      <div className="flex items-center justify-between sticky top-0 bg-background z-10 py-2">
        <h3 className="text-lg font-medium">Weight Range Configuration</h3>
        <AddWeightRangePopover />
      </div>

      {weightRanges.map((range) => {
        const rates = getRatesForRange(range);
        const headerLabel = formatRangeLabel(range.min_weight, range.max_weight);

        return (
          <div
            key={`${range.min_weight}-${range.max_weight}`}
            className="bg-card border border-border rounded-lg shadow-sm"
          >
            {/* Header */}
            <div className="px-4 py-3 border-b border-border flex items-center justify-between">
              <h4 className="font-semibold text-foreground text-sm">
                {headerLabel}
                <span className="ml-2 text-xs font-normal text-muted-foreground">
                  ({rates.length} rate{rates.length !== 1 ? "s" : ""})
                </span>
              </h4>
              <button
                onClick={() => onRemoveWeightRange(range.min_weight, range.max_weight)}
                className="p-1.5 text-muted-foreground hover:text-destructive hover:bg-destructive/10 rounded transition-colors"
                title="Remove Weight Range"
              >
                <TrashIcon className="h-4 w-4" />
              </button>
            </div>

            {/* Rate entries table */}
            {rates.length > 0 ? (
              <div className="overflow-x-auto">
                <table className="w-full text-sm">
                  <thead>
                    <tr className="border-b border-border bg-muted/30">
                      <th className="px-4 py-2 text-left text-xs font-medium text-muted-foreground">
                        Service
                      </th>
                      <th className="px-4 py-2 text-left text-xs font-medium text-muted-foreground">
                        Zone
                      </th>
                      <th className="px-4 py-2 text-right text-xs font-medium text-muted-foreground">
                        Rate
                      </th>
                      <th className="px-4 py-2 text-right text-xs font-medium text-muted-foreground">
                        Cost
                      </th>
                      <th className="px-4 py-2 text-right text-xs font-medium text-muted-foreground">
                        Transit Days
                      </th>
                      <th className="px-4 py-2 text-right text-xs font-medium text-muted-foreground">
                        Transit Time
                      </th>
                      {onEditRate && (
                        <th className="px-4 py-2 w-10" />
                      )}
                    </tr>
                  </thead>
                  <tbody>
                    {rates.map((sr, idx) => (
                      <tr
                        key={`${sr.service_id}-${sr.zone_id}-${idx}`}
                        className="border-b border-border last:border-0 hover:bg-accent/50 transition-colors"
                      >
                        <td className="px-4 py-2 text-foreground font-medium truncate max-w-[200px]">
                          {getServiceName(sr.service_id)}
                        </td>
                        <td className="px-4 py-2 text-foreground truncate max-w-[120px]">
                          {getZoneLabel(sr.zone_id)}
                        </td>
                        <td className="px-4 py-2 text-right font-mono text-foreground">
                          {sr.rate > 0 ? sr.rate.toFixed(2) : "\u2014"}
                        </td>
                        <td className="px-4 py-2 text-right font-mono text-muted-foreground">
                          {sr.cost != null && sr.cost > 0
                            ? sr.cost.toFixed(2)
                            : "\u2014"}
                        </td>
                        <td className="px-4 py-2 text-right text-muted-foreground">
                          {sr.transit_days != null ? sr.transit_days : "\u2014"}
                        </td>
                        <td className="px-4 py-2 text-right text-muted-foreground">
                          {sr.transit_time != null
                            ? `${sr.transit_time}h`
                            : "\u2014"}
                        </td>
                        {onEditRate && (
                          <td className="px-2 py-2">
                            <button
                              onClick={() => onEditRate(sr)}
                              className="p-1 text-muted-foreground hover:text-foreground hover:bg-accent rounded transition-colors"
                              title="Edit Rate"
                            >
                              <Pencil1Icon className="h-3.5 w-3.5" />
                            </button>
                          </td>
                        )}
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            ) : (
              <div className="px-4 py-6 text-center text-xs text-muted-foreground">
                No rate entries for this weight range
              </div>
            )}
          </div>
        );
      })}
    </div>
  );
}

export default WeightRangesTab;
