"use client";

import React from "react";
import { PlusIcon, Pencil1Icon, TrashIcon } from "@radix-ui/react-icons";
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "@karrio/ui/components/ui/popover";
import type {
  EmbeddedZone,
  ServiceLevelWithZones,
} from "@karrio/ui/components/rate-sheet-editor";

interface MultiSelectOption {
  value: string;
  label: string;
}

interface ZonePreset {
  id: string;
  label: string;
  countries: number;
}

interface ZonesTabProps {
  services: ServiceLevelWithZones[];
  sharedZonesFromParent?: EmbeddedZone[];
  onUpdateZone: (zoneLabel: string, updates: Partial<EmbeddedZone>) => void;
  onEditZone: (zone: EmbeddedZone) => void;
  onAddZone: () => void;
  onRemoveZone: (zoneLabel: string) => void;
  countryOptions: MultiSelectOption[];
  zonePresets?: ZonePreset[];
  onAddZoneFromPreset?: (presetZoneId: string) => void;
  onCloneZone?: (zone: EmbeddedZone) => void;
}

export function ZonesTab({
  services,
  sharedZonesFromParent = [],
  onEditZone,
  onAddZone,
  onRemoveZone,
  zonePresets,
  onAddZoneFromPreset,
  onCloneZone,
}: ZonesTabProps) {
  // Build combined zones list from service zones first, then unlinked zones from parent
  const zones = (() => {
    const zonesMap = new Map<string, EmbeddedZone>();
    const orderedZones: EmbeddedZone[] = [];

    services.flatMap((s) => s.zones || []).forEach((zone) => {
      const key = zone.label || zone.id;
      if (!zonesMap.has(key)) {
        zonesMap.set(key, zone);
        orderedZones.push(zone);
      }
    });

    sharedZonesFromParent.forEach((zone) => {
      const key = zone.label || zone.id;
      if (!zonesMap.has(key)) {
        zonesMap.set(key, zone);
        orderedZones.push(zone);
      }
    });

    return orderedZones;
  })();

  // Count how many services link to a given zone
  const getLinkedServicesCount = (zone: EmbeddedZone): number => {
    return services.filter((s) =>
      (s.zones || []).some((z) => z.id === zone.id || z.label === zone.label)
    ).length;
  };

  // Format country codes for display
  const formatCountries = (codes?: string[]): string => {
    if (!codes || codes.length === 0) return "\u2014";
    if (codes.length <= 4) return codes.join(", ");
    return `${codes.slice(0, 4).join(", ")} (+${codes.length - 4})`;
  };

  const AddZonePopover = ({ align = "end" }: { align?: "start" | "end" | "center" }) => (
    <Popover>
      <PopoverTrigger asChild>
        <button className="inline-flex items-center gap-2 px-4 py-2 text-sm font-medium text-primary-foreground bg-primary hover:bg-primary/90 rounded-md transition-colors">
          <PlusIcon className="h-4 w-4" />
          Add Zone
        </button>
      </PopoverTrigger>
      <PopoverContent align={align} className="w-56 p-2" sideOffset={8}>
        <div className="space-y-1">
          <p className="text-xs font-medium text-muted-foreground px-2 py-1">Add zone</p>

          {zonePresets && zonePresets.length > 0 && (
            <>
              <div className="max-h-48 overflow-y-auto space-y-0.5">
                {zonePresets.map((preset) => (
                  <button
                    key={preset.id}
                    onClick={() => onAddZoneFromPreset?.(preset.id)}
                    className="w-full text-left px-2 py-1.5 text-sm rounded-md hover:bg-accent transition-colors truncate"
                    title={`${preset.label} (${preset.countries} countries)`}
                  >
                    {preset.label}
                  </button>
                ))}
              </div>
              <div className="border-t border-border my-1" />
            </>
          )}

          {zones.length > 0 && onCloneZone && (
            <>
              <p className="text-xs text-muted-foreground px-2 py-0.5">Clone existing</p>
              <div className="max-h-32 overflow-y-auto space-y-0.5">
                {zones.map((zone) => (
                  <button
                    key={zone.id}
                    onClick={() => onCloneZone(zone)}
                    className="w-full text-left px-2 py-1.5 text-sm rounded-md hover:bg-accent transition-colors truncate text-muted-foreground"
                    title={`Clone ${zone.label}`}
                  >
                    {zone.label}
                  </button>
                ))}
              </div>
              <div className="border-t border-border my-1" />
            </>
          )}

          <button
            onClick={onAddZone}
            className="w-full text-left px-2 py-1.5 text-sm rounded-md hover:bg-accent transition-colors flex items-center gap-1.5 text-primary font-medium"
          >
            <PlusIcon className="h-3.5 w-3.5" />
            Create new zone
          </button>
        </div>
      </PopoverContent>
    </Popover>
  );

  if (zones.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center h-full text-muted-foreground p-8">
        <p className="mb-4">No zones configured yet.</p>
        <AddZonePopover align="center" />
      </div>
    );
  }

  return (
    <div className="space-y-4 h-full overflow-y-auto pr-2">
      <div className="flex items-center justify-between sticky top-0 bg-background z-10 py-2">
        <h3 className="text-lg font-medium">Zone Configuration</h3>
        <AddZonePopover />
      </div>

      {zones.map((zone, index) => {
        const zoneKey = zone.label || zone.id;
        const linkedCount = getLinkedServicesCount(zone);
        const countriesDisplay = formatCountries(zone.country_codes);
        const hasCities = zone.cities && zone.cities.length > 0;
        const hasPostalCodes = zone.postal_codes && zone.postal_codes.length > 0;

        return (
          <div
            key={zone.id || index}
            className="bg-card border border-border rounded-lg shadow-sm hover:border-primary/50 transition-colors"
          >
            <div className="px-6 py-4 space-y-4">
              {/* Header with zone name and actions */}
              <div className="flex items-center justify-between gap-4">
                <h4 className="font-semibold text-foreground text-base">
                  {zone.label || `Zone ${index + 1}`}
                </h4>
                <div className="flex items-center gap-1">
                  <button
                    onClick={() => onEditZone(zone)}
                    className="p-1.5 text-muted-foreground hover:text-foreground hover:bg-accent rounded transition-colors"
                    title="Edit Zone"
                  >
                    <Pencil1Icon className="h-4 w-4" />
                  </button>
                  <button
                    onClick={() => onRemoveZone(zoneKey)}
                    className="p-1.5 text-muted-foreground hover:text-destructive hover:bg-destructive/10 rounded transition-colors"
                    title="Delete Zone"
                  >
                    <TrashIcon className="h-4 w-4" />
                  </button>
                </div>
              </div>

              {/* Zone details grid */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-x-12 gap-y-4">
                <div className="flex items-center gap-2">
                  <div className="text-sm font-medium text-muted-foreground whitespace-nowrap">
                    Countries:
                  </div>
                  <div className="text-sm font-semibold text-foreground truncate">
                    {countriesDisplay}
                  </div>
                </div>

                <div className="flex items-center gap-2">
                  <div className="text-sm font-medium text-muted-foreground whitespace-nowrap">
                    Transit Days:
                  </div>
                  <div className="text-sm font-semibold text-foreground">
                    {zone.transit_days ?? "\u2014"}
                  </div>
                </div>

                <div className="flex items-center gap-2">
                  <div className="text-sm font-medium text-muted-foreground whitespace-nowrap">
                    Cities:
                  </div>
                  <div className="text-sm font-semibold text-foreground truncate">
                    {hasCities ? zone.cities!.join(", ") : "\u2014"}
                  </div>
                </div>

                <div className="flex items-center gap-2">
                  <div className="text-sm font-medium text-muted-foreground whitespace-nowrap">
                    Postal Codes:
                  </div>
                  <div className="text-sm font-semibold text-foreground truncate">
                    {hasPostalCodes ? zone.postal_codes!.join(", ") : "\u2014"}
                  </div>
                </div>

                <div className="flex items-center gap-2">
                  <div className="text-sm font-medium text-muted-foreground whitespace-nowrap">
                    Linked Services:
                  </div>
                  <div className="text-sm font-semibold text-foreground">
                    {linkedCount} of {services.length}
                  </div>
                </div>
              </div>
            </div>
          </div>
        );
      })}
    </div>
  );
}

export default ZonesTab;
