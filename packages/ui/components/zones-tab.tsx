"use client";

import React from "react";
import { Button } from "@karrio/ui/components/ui/button";
import { Input } from "@karrio/ui/components/ui/input";
import { Label } from "@karrio/ui/components/ui/label";
import { MultiSelect } from "@karrio/ui/components/multi-select";
import { PlusIcon, TrashIcon } from "@radix-ui/react-icons";
import type {
  EmbeddedZone,
  ServiceLevelWithZones,
} from "@karrio/ui/components/rate-sheet-editor";

interface MultiSelectOption {
  value: string;
  label: string;
}

interface ZonesTabProps {
  services: ServiceLevelWithZones[];
  sharedZonesFromParent?: EmbeddedZone[];
  onUpdateZone: (zoneLabel: string, updates: Partial<EmbeddedZone>) => void;
  onAddZone: () => void;
  onRemoveZone: (zoneLabel: string) => void;
  countryOptions: MultiSelectOption[];
  getZoneTextValue?: (
    zoneLabel: string,
    field: "cities" | "postal_codes",
    currentArray: string[] | undefined | null
  ) => string;
  setZoneTextValue?: (
    zoneLabel: string,
    field: "cities" | "postal_codes",
    text: string
  ) => void;
  persistZoneTextValue?: (
    zoneLabel: string,
    field: "cities" | "postal_codes"
  ) => void;
}

export function ZonesTab({
  services,
  sharedZonesFromParent = [],
  onUpdateZone,
  onAddZone,
  onRemoveZone,
  countryOptions,
  getZoneTextValue,
  setZoneTextValue,
  persistZoneTextValue,
}: ZonesTabProps) {
  // Build combined zones list from service zones first, then unlinked zones from parent
  const zones = React.useMemo(() => {
    const zonesMap = new Map<string, EmbeddedZone>();
    const orderedZones: EmbeddedZone[] = [];

    // Add linked zones from services first (maintains their order)
    services.flatMap((s) => s.zones || []).forEach((zone) => {
      const key = zone.label || zone.id;
      if (!zonesMap.has(key)) {
        zonesMap.set(key, zone);
        orderedZones.push(zone);
      }
    });

    // Then add unlinked zones from parent (these are newly added zones - appear at end)
    sharedZonesFromParent.forEach((zone) => {
      const key = zone.label || zone.id;
      if (!zonesMap.has(key)) {
        zonesMap.set(key, zone);
        orderedZones.push(zone);
      }
    });

    return orderedZones;
  }, [services, sharedZonesFromParent]);

  if (zones.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center h-full text-muted-foreground p-8">
        <p className="mb-4">No zones configured yet.</p>
        <Button onClick={onAddZone}>
          <PlusIcon className="h-4 w-4 mr-2" />
          Add Zone
        </Button>
      </div>
    );
  }

  return (
    <div className="space-y-6 h-full overflow-y-auto pr-2">
      <div className="flex items-center justify-between sticky top-0 bg-background z-10 py-2">
        <h3 className="text-lg font-medium">Zone Configuration</h3>
        <Button onClick={onAddZone}>
          <PlusIcon className="h-4 w-4 mr-2" />
          Add Zone
        </Button>
      </div>

      <div className="grid gap-4 grid-cols-1 pb-6">
        {zones.map((zone, index) => {
          const zoneKey = zone.label || zone.id;
          return (
            <div
              key={zone.id || index}
              className="p-4 bg-card border border-border rounded-lg shadow-sm space-y-4 relative group"
            >
              <div className="flex items-center justify-between gap-2">
                <h4 className="text-base font-semibold text-foreground">
                  {zone.label || `Zone ${index + 1}`}
                </h4>
                <Button
                  variant="ghost"
                  size="icon"
                  onClick={() => onRemoveZone(zoneKey)}
                  className="text-muted-foreground hover:text-destructive"
                >
                  <TrashIcon className="h-4 w-4" />
                </Button>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-x-6 gap-y-3">
                <div>
                  <Label className="text-xs mb-1 block">Label</Label>
                  <Input
                    value={zone.label || ""}
                    onChange={(e) =>
                      onUpdateZone(zoneKey, { label: e.target.value })
                    }
                    placeholder={`Zone ${index + 1}`}
                  />
                </div>

                <div>
                  <Label className="text-xs mb-1 block">Country Codes</Label>
                  <MultiSelect
                    options={countryOptions}
                    value={zone.country_codes || []}
                    onValueChange={(vals) => {
                      const unique = Array.from(
                        new Set(vals.map((v) => v.toUpperCase()))
                      );
                      onUpdateZone(zoneKey, { country_codes: unique });
                    }}
                    placeholder="Select countries"
                  />
                </div>

                <div>
                  <Label className="text-xs mb-1 block">
                    Cities (comma separated)
                  </Label>
                  <Input
                    value={
                      getZoneTextValue && setZoneTextValue && persistZoneTextValue
                        ? getZoneTextValue(zoneKey, "cities", zone.cities)
                        : zone.cities?.join(", ") || ""
                    }
                    onChange={(e) => {
                      if (setZoneTextValue) {
                        setZoneTextValue(zoneKey, "cities", e.target.value);
                      } else {
                        onUpdateZone(zoneKey, {
                          cities: e.target.value
                            .split(",")
                            .map((s) => s.trim())
                            .filter(Boolean),
                        });
                      }
                    }}
                    onBlur={() => {
                      if (persistZoneTextValue) {
                        persistZoneTextValue(zoneKey, "cities");
                      }
                    }}
                    placeholder="New York, Toronto"
                  />
                </div>

                <div>
                  <Label className="text-xs mb-1 block">
                    Postal Codes (comma separated)
                  </Label>
                  <Input
                    value={
                      getZoneTextValue && setZoneTextValue && persistZoneTextValue
                        ? getZoneTextValue(
                            zoneKey,
                            "postal_codes",
                            zone.postal_codes
                          )
                        : zone.postal_codes?.join(", ") || ""
                    }
                    onChange={(e) => {
                      if (setZoneTextValue) {
                        setZoneTextValue(zoneKey, "postal_codes", e.target.value);
                      } else {
                        onUpdateZone(zoneKey, {
                          postal_codes: e.target.value
                            .split(",")
                            .map((s) => s.trim())
                            .filter(Boolean),
                        });
                      }
                    }}
                    onBlur={() => {
                      if (persistZoneTextValue) {
                        persistZoneTextValue(zoneKey, "postal_codes");
                      }
                    }}
                    placeholder="10001, 94105"
                  />
                </div>

                <div>
                  <Label className="text-xs mb-1 block">Transit Days</Label>
                  <Input
                    type="number"
                    min={0}
                    value={zone.transit_days?.toString() || ""}
                    onChange={(e) => {
                      const val = e.target.value;
                      const parsed = val ? parseInt(val, 10) : null;
                      const sanitized =
                        parsed !== null && parsed < 0 ? 0 : parsed;
                      onUpdateZone(zoneKey, { transit_days: sanitized });
                    }}
                    placeholder="2"
                  />
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}

export default ZonesTab;
