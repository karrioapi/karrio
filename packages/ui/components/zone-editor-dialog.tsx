"use client";

import React, { useEffect, useState } from "react";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogFooter,
  DialogTitle,
  DialogDescription,
  DialogBody,
} from "@karrio/ui/components/ui/dialog";
import { Button } from "@karrio/ui/components/ui/button";
import { Input } from "@karrio/ui/components/ui/input";
import { Label } from "@karrio/ui/components/ui/label";
import { Checkbox } from "@karrio/ui/components/ui/checkbox";
import { MultiSelect } from "@karrio/ui/components/multi-select";
import type {
  EmbeddedZone,
  ServiceLevelWithZones,
} from "@karrio/ui/components/rate-sheet-editor";

interface MultiSelectOption {
  value: string;
  label: string;
}

interface ZoneEditorDialogProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  zone: EmbeddedZone | null;
  onSave: (zoneLabel: string, updates: Partial<EmbeddedZone>) => void;
  countryOptions: MultiSelectOption[];
  services: ServiceLevelWithZones[];
  onToggleServiceZone?: (serviceId: string, zoneId: string, linked: boolean) => void;
}

export function ZoneEditorDialog({
  open,
  onOpenChange,
  zone,
  onSave,
  countryOptions,
  services,
  onToggleServiceZone,
}: ZoneEditorDialogProps) {
  const [label, setLabel] = useState("");
  const [countryCodes, setCountryCodes] = useState<string[]>([]);
  const [citiesText, setCitiesText] = useState("");
  const [postalCodesText, setPostalCodesText] = useState("");
  const [transitDays, setTransitDays] = useState<string>("");

  useEffect(() => {
    if (zone && open) {
      setLabel(zone.label || "");
      setCountryCodes(zone.country_codes || []);
      setCitiesText(zone.cities?.join(", ") || "");
      setPostalCodesText(zone.postal_codes?.join(", ") || "");
      setTransitDays(zone.transit_days?.toString() || "");
    }
  }, [zone, open]);

  const isServiceLinked = (serviceId: string): boolean => {
    const service = services.find((s) => s.id === serviceId);
    if (!service || !zone) return false;
    return (service.zones || []).some((z) => z.id === zone.id || z.label === zone.label);
  };

  const getLinkedServicesCount = (): number => {
    if (!zone) return 0;
    return services.filter((s) =>
      (s.zones || []).some((z) => z.id === zone.id || z.label === zone.label)
    ).length;
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!zone) return;

    const zoneKey = zone.label || zone.id;
    const cities = citiesText
      .split(",")
      .map((s) => s.trim())
      .filter(Boolean);
    const postalCodes = postalCodesText
      .split(",")
      .map((s) => s.trim())
      .filter(Boolean);
    const parsed = transitDays ? parseInt(transitDays, 10) : null;
    const sanitized = parsed !== null && parsed < 0 ? 0 : parsed;

    onSave(zoneKey, {
      label,
      country_codes: Array.from(new Set(countryCodes.map((v) => v.toUpperCase()))),
      cities,
      postal_codes: postalCodes,
      transit_days: sanitized,
    });
    onOpenChange(false);
  };

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="max-w-lg">
        <DialogHeader>
          <DialogTitle>Edit Zone</DialogTitle>
          <DialogDescription>
            Configure zone details and linked services
          </DialogDescription>
        </DialogHeader>

        <DialogBody>
          <form id="zone-form" onSubmit={handleSubmit} className="space-y-4">
            <div className="space-y-1.5">
              <Label className="text-xs">Label</Label>
              <Input
                value={label}
                onChange={(e) => setLabel(e.target.value)}
                placeholder="Zone 1"
                className="h-9"
              />
            </div>

            <div className="space-y-1.5">
              <Label className="text-xs">Transit Days</Label>
              <Input
                type="number"
                min={0}
                value={transitDays}
                onChange={(e) => setTransitDays(e.target.value)}
                placeholder="2"
                className="h-9"
              />
            </div>

            <div className="space-y-1.5">
              <Label className="text-xs">Country Codes</Label>
              <MultiSelect
                options={countryOptions}
                value={countryCodes}
                onValueChange={setCountryCodes}
                placeholder="Select countries"
              />
            </div>

            <div className="space-y-1.5">
              <Label className="text-xs">Cities (comma separated)</Label>
              <Input
                value={citiesText}
                onChange={(e) => setCitiesText(e.target.value)}
                placeholder="New York, Toronto"
                className="h-9"
              />
            </div>

            <div className="space-y-1.5">
              <Label className="text-xs">Postal Codes (comma separated)</Label>
              <Input
                value={postalCodesText}
                onChange={(e) => setPostalCodesText(e.target.value)}
                placeholder="10001, 94105"
                className="h-9"
              />
            </div>

            {/* Service Linking Section */}
            {services.length > 0 && onToggleServiceZone && zone && (
              <div className="pt-3 border-t border-border">
                <Label className="text-xs text-muted-foreground block mb-2">
                  Linked Services ({getLinkedServicesCount()} of {services.length})
                </Label>
                <div className="space-y-2 max-h-40 overflow-y-auto">
                  {services.map((service) => {
                    const linked = isServiceLinked(service.id);
                    const checkId = `zone-svc-${service.id}`;
                    return (
                      <label
                        key={service.id}
                        htmlFor={checkId}
                        className="flex items-center gap-2.5 px-2 py-1.5 rounded-md hover:bg-accent cursor-pointer transition-colors"
                      >
                        <Checkbox
                          id={checkId}
                          checked={linked}
                          onCheckedChange={(checked) =>
                            onToggleServiceZone(service.id, zone.id, checked === true)
                          }
                        />
                        <span className="text-sm text-foreground">
                          {service.service_name || service.service_code}
                        </span>
                      </label>
                    );
                  })}
                </div>
              </div>
            )}
          </form>
        </DialogBody>

        <DialogFooter>
          <Button type="button" variant="outline" size="sm" onClick={() => onOpenChange(false)}>
            Cancel
          </Button>
          <Button type="submit" size="sm" form="zone-form">
            Save
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}

export default ZoneEditorDialog;
