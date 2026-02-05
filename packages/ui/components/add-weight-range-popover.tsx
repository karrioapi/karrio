"use client";

import { PlusIcon } from "@radix-ui/react-icons";
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "@karrio/ui/components/ui/popover";
import type { WeightRange } from "@karrio/ui/components/weight-rate-grid";

interface WeightRangePreset {
  min_weight: number;
  max_weight: number;
}

interface AddWeightRangePopoverProps {
  onAddWeightRange: () => void;
  weightUnit: string;
  weightRangePresets?: WeightRangePreset[];
  onAddFromPreset?: (minWeight: number, maxWeight: number) => void;
  missingRanges?: WeightRange[];
  onAddMissingRange?: (minWeight: number, maxWeight: number) => void;
  align?: "start" | "end" | "center";
}

const formatRangeLabel = (min: number, max: number, unit: string) =>
  min === 0 ? `Up to ${max} ${unit}` : `${min} \u2013 ${max} ${unit}`;

export function AddWeightRangePopover({
  onAddWeightRange,
  weightUnit,
  weightRangePresets,
  onAddFromPreset,
  missingRanges,
  onAddMissingRange,
  align = "start",
}: AddWeightRangePopoverProps) {
  return (
    <Popover>
      <PopoverTrigger asChild>
        <button className="flex items-center gap-1 px-3 py-1.5 text-xs font-medium text-primary hover:bg-accent rounded-md transition-colors">
          <PlusIcon className="h-3 w-3" />
          Add Weight Range
        </button>
      </PopoverTrigger>
      <PopoverContent align={align} className="w-60 p-2" sideOffset={8}>
        <div className="space-y-1">
          <p className="text-xs font-medium text-muted-foreground px-2 py-1">
            Add weight range
          </p>

          {/* Missing ranges for this service */}
          {missingRanges && missingRanges.length > 0 && onAddMissingRange && (
            <>
              <p className="text-xs text-muted-foreground px-2 py-0.5">
                Missing from this service
              </p>
              <div className="max-h-32 overflow-y-auto space-y-0.5">
                {missingRanges.map((range) => (
                  <button
                    key={`${range.min_weight}-${range.max_weight}`}
                    onClick={() =>
                      onAddMissingRange(range.min_weight, range.max_weight)
                    }
                    className="w-full text-left px-2 py-1.5 text-sm rounded-md hover:bg-accent transition-colors truncate text-amber-600 dark:text-amber-400"
                    title={formatRangeLabel(
                      range.min_weight,
                      range.max_weight,
                      weightUnit
                    )}
                  >
                    {formatRangeLabel(
                      range.min_weight,
                      range.max_weight,
                      weightUnit
                    )}
                  </button>
                ))}
              </div>
              <div className="border-t border-border my-1" />
            </>
          )}

          {/* Carrier presets */}
          {weightRangePresets &&
            weightRangePresets.length > 0 &&
            onAddFromPreset && (
              <>
                <p className="text-xs text-muted-foreground px-2 py-0.5">
                  Carrier presets
                </p>
                <div className="max-h-48 overflow-y-auto space-y-0.5">
                  {weightRangePresets.map((preset) => (
                    <button
                      key={`${preset.min_weight}-${preset.max_weight}`}
                      onClick={() =>
                        onAddFromPreset(preset.min_weight, preset.max_weight)
                      }
                      className="w-full text-left px-2 py-1.5 text-sm rounded-md hover:bg-accent transition-colors truncate"
                      title={formatRangeLabel(
                        preset.min_weight,
                        preset.max_weight,
                        weightUnit
                      )}
                    >
                      {formatRangeLabel(
                        preset.min_weight,
                        preset.max_weight,
                        weightUnit
                      )}
                    </button>
                  ))}
                </div>
                <div className="border-t border-border my-1" />
              </>
            )}

          {/* Custom range */}
          <button
            onClick={onAddWeightRange}
            className="w-full text-left px-2 py-1.5 text-sm rounded-md hover:bg-accent transition-colors flex items-center gap-1.5 text-primary font-medium"
          >
            <PlusIcon className="h-3.5 w-3.5" />
            Custom range
          </button>
        </div>
      </PopoverContent>
    </Popover>
  );
}
