"use client";

import React, { useRef, useState, useEffect, useMemo } from "react";
import { useVirtualizer } from "@tanstack/react-virtual";
import { Button } from "@karrio/ui/components/ui/button";
import { PlusIcon, Cross2Icon, MinusIcon } from "@radix-ui/react-icons";
import { cn } from "@karrio/ui/lib/utils";
import type {
  ServiceLevelWithZones,
  EmbeddedZone,
} from "@karrio/ui/components/rate-sheet-editor";

// Generate a unique ID for new zones
const generateId = (prefix: string = "zone") =>
  `${prefix}-${crypto.randomUUID()}`;

interface RateSheetTableProps {
  services: ServiceLevelWithZones[];
  // Shared zones from parent state (zones that may not be linked to any service)
  sharedZonesFromParent?: EmbeddedZone[];
  onUpdateService: (index: number, service: ServiceLevelWithZones) => void;
  onAddZone: () => void;
  onRemoveZone: (zoneLabel: string) => void;
  // Optional: Callback to link/unlink zone to service
  onToggleZoneService?: (
    serviceIndex: number,
    zoneId: string,
    linked: boolean,
    zoneLabel: string
  ) => void;
}

// Cell for editing rate values
const EditableCell = React.memo(
  ({
    value,
    onSave,
    disabled = false,
    type = "number",
    isLinked = true,
    onLink,
    onUnlink,
  }: {
    value: number | null | undefined;
    onSave: (value: string) => void;
    disabled?: boolean;
    type?: "number" | "text";
    isLinked?: boolean;
    onLink?: () => void;
    onUnlink?: () => void;
  }) => {
    const [isEditing, setIsEditing] = useState(false);
    const [editValue, setEditValue] = useState(value?.toString() || "");
    const [localValue, setLocalValue] = useState(value?.toString() || "");
    const inputRef = useRef<HTMLInputElement>(null);

    // Update local value when prop value changes
    useEffect(() => {
      setLocalValue(value?.toString() || "");
      if (!isEditing) {
        setEditValue(value?.toString() || "");
      }
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
        setLocalValue(editValue); // Optimistically update
      }
      setIsEditing(false);
    };

    const handleKeyDown = (e: React.KeyboardEvent) => {
      if (e.key === "Enter") {
        handleSave();
      } else if (e.key === "Escape") {
        setEditValue(localValue);
        setIsEditing(false);
      }
    };

    // Handle unlinked cell - show plus button to link
    if (!isLinked && onLink) {
      return (
        <div
          className="w-full h-full px-2 py-2 text-center flex items-center justify-center group"
          title="Click to add rate for this zone"
        >
          <button
            onClick={onLink}
            className="p-1 text-muted-foreground/50 hover:text-primary hover:bg-accent rounded opacity-0 group-hover:opacity-100 transition-opacity"
          >
            <PlusIcon className="h-4 w-4" />
          </button>
        </div>
      );
    }

    if (isEditing) {
      return (
        <input
          ref={inputRef}
          type={type}
          step={type === "number" ? "any" : undefined}
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
          "w-full h-full px-2 py-2 text-center text-sm text-muted-foreground cursor-pointer hover:bg-accent flex items-center justify-center group relative",
          disabled && "cursor-not-allowed opacity-50"
        )}
        onClick={() => !disabled && setIsEditing(true)}
        title={disabled ? "Read only" : "Click to edit"}
      >
        <span>
          {value != null && !isNaN(Number(localValue))
            ? Number(localValue).toFixed(2)
            : "-"}
        </span>
        {/* Unlink button - shows on hover */}
        {onUnlink && (
          <button
            onClick={(e) => {
              e.stopPropagation();
              onUnlink();
            }}
            className="absolute right-1 top-1/2 -translate-y-1/2 p-0.5 text-muted-foreground/50 hover:text-destructive hover:bg-destructive/10 rounded opacity-0 group-hover:opacity-100 transition-opacity"
            title="Remove zone from this service"
          >
            <MinusIcon className="h-3 w-3" />
          </button>
        )}
      </div>
    );
  }
);

EditableCell.displayName = "EditableCell";

export function RateSheetTable({
  services,
  sharedZonesFromParent = [],
  onUpdateService,
  onAddZone,
  onRemoveZone,
  onToggleZoneService,
}: RateSheetTableProps) {
  const parentRef = useRef<HTMLDivElement>(null);

  // Virtualizer for rows (services)
  const rowVirtualizer = useVirtualizer({
    count: services.length,
    getScrollElement: () => parentRef.current,
    estimateSize: () => 48, // Extra room for service code line
    overscan: 5,
  });

  // Build shared zones list combining zones from services first, then unlinked zones from parent (deduped by label)
  // Maintains insertion order - new zones appear at the end (rightmost column)
  const sharedZones = useMemo((): EmbeddedZone[] => {
    const zoneMap = new Map<string, EmbeddedZone>();
    const orderedZones: EmbeddedZone[] = [];

    // Add linked zones from services first (maintains their order)
    services
      .flatMap((s) => s.zones || [])
      .forEach((zone) => {
        const key = zone.label || zone.id;
        if (!zoneMap.has(key)) {
          zoneMap.set(key, zone);
          orderedZones.push(zone);
        }
      });

    // Then add unlinked zones from parent (these are newly added zones - appear at end)
    sharedZonesFromParent.forEach((zone) => {
      const key = zone.label || zone.id;
      if (!zoneMap.has(key)) {
        zoneMap.set(key, zone);
        orderedZones.push(zone);
      }
    });

    return orderedZones;
  }, [services, sharedZonesFromParent]);

  // Build a map to quickly find a service's zone by zone label
  const getServiceZone = (
    service: ServiceLevelWithZones,
    zoneLabel: string
  ): EmbeddedZone | null => {
    return (service.zones || []).find((z) => z.label === zoneLabel) || null;
  };

  // Handle cell save - update rate for specific zone in a service
  const handleCellSave = (
    serviceIndex: number,
    zoneLabel: string,
    newValue: string
  ) => {
    const service = services[serviceIndex];
    const newRate = parseFloat(newValue);

    if (!isNaN(newRate) && service.zones) {
      const updatedZones = service.zones.map((zone) => {
        if (zone.label === zoneLabel) {
          return { ...zone, rate: newRate };
        }
        return zone;
      });
      onUpdateService(serviceIndex, {
        ...service,
        zones: updatedZones,
      });
    }
  };

  // Handle linking a zone to a service (add zone with default rate)
  const handleLinkZone = (serviceIndex: number, zone: EmbeddedZone) => {
    const service = services[serviceIndex];
    // Add the zone to this service's zones array
    const newZone: EmbeddedZone = {
      ...zone,
      id: generateId("zone"),
      rate: 0, // Default rate
    };
    const updatedZones = [...(service.zones || []), newZone];
    onUpdateService(serviceIndex, {
      ...service,
      zones: updatedZones,
    });
    // Also call the callback if provided
    if (onToggleZoneService) {
      onToggleZoneService(serviceIndex, zone.id, true, zone.label);
    }
  };

  // Handle unlinking a zone from a service (remove zone)
  const handleUnlinkZone = (serviceIndex: number, zoneLabel: string) => {
    const service = services[serviceIndex];
    const zoneToRemove = getServiceZone(service, zoneLabel);
    if (!zoneToRemove) return;

    const updatedZones = (service.zones || []).filter(
      (z) => z.label !== zoneLabel
    );
    onUpdateService(serviceIndex, {
      ...service,
      zones: updatedZones,
    });
    // Also call the callback if provided
    if (onToggleZoneService) {
      onToggleZoneService(serviceIndex, zoneToRemove.id, false, zoneLabel);
    }
  };

  // Calculate total table width for proper scrolling
  const tableWidth = 192 + sharedZones.length * 128; // service col + zones

  if (services.length === 0) {
    return (
      <div className="flex-1 flex items-center justify-center text-muted-foreground bg-muted/50 rounded border-2 border-dashed">
        <div className="text-center p-8">
          <p className="text-lg mb-2">No services configured</p>
          <p className="text-sm mb-4">
            Go to the Services tab to add services first
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="h-full flex flex-col">
      {/* Table container with border */}
      <div className="flex-1 flex flex-col border border-border rounded-md bg-background overflow-hidden">
        {/* Single scroll container for both header and body */}
        <div ref={parentRef} className="flex-1 overflow-auto">
          {/* Table with minimum width to enable horizontal scroll */}
          <div style={{ minWidth: `${tableWidth}px` }}>
            {/* Table Header - Sticky top */}
            <div className="flex border-b border-border bg-muted font-medium text-sm text-foreground sticky top-0 z-30 shadow-sm">
              {/* Service Name Column Header - Sticky left + top (corner cell) */}
              <div className="w-48 p-3 border-r border-border flex-shrink-0 bg-muted sticky left-0 z-40 shadow-[2px_0_5px_-2px_rgba(0,0,0,0.1)]">
                Service Level
              </div>

              {/* Zone Headers - shows all shared zones */}
              {sharedZones.map((zone, index) => (
                <div
                  key={zone.label || zone.id || index}
                  className="w-32 p-3 border-r border-border flex-shrink-0 flex items-center justify-between group relative bg-muted"
                >
                  <span
                    className="truncate"
                    title={zone.label || `Zone ${index + 1}`}
                  >
                    {zone.label || `Zone ${index + 1}`}
                  </span>
                  <button
                    onClick={() => onRemoveZone(zone.label || zone.id)}
                    className="opacity-0 group-hover:opacity-100 p-1 hover:bg-accent rounded text-muted-foreground hover:text-destructive transition-opacity"
                    title="Remove Zone"
                  >
                    <Cross2Icon className="h-3 w-3" />
                  </button>
                </div>
              ))}
            </div>

            {/* Virtualized Body */}
            <div
              style={{
                height: `${rowVirtualizer.getTotalSize()}px`,
                position: "relative",
              }}
            >
              {rowVirtualizer.getVirtualItems().map((virtualRow) => {
                const service = services[virtualRow.index];
                return (
                  <div
                    key={virtualRow.key}
                    className="absolute top-0 left-0 w-full flex border-b border-border hover:bg-muted/50 transition-colors"
                    style={{
                      height: `${virtualRow.size}px`,
                      transform: `translateY(${virtualRow.start}px)`,
                    }}
                  >
                    {/* Service Name Column - Sticky left with shadow */}
                    <div className="w-48 px-3 py-2 border-r border-border flex-shrink-0 bg-background sticky left-0 z-20 flex flex-col justify-center shadow-[2px_0_5px_-2px_rgba(0,0,0,0.1)]">
                      <div className="flex flex-col leading-tight gap-px">
                        <span
                          className="text-sm font-semibold text-foreground truncate"
                          title={service.service_name || ""}
                        >
                          {service.service_name || "Unnamed service"}
                        </span>
                        {service.service_code && (
                          <span
                            className="text-xs text-muted-foreground truncate"
                            title={service.service_code}
                          >
                            {service.service_code}
                          </span>
                        )}
                      </div>
                    </div>

                    {/* Rate Cells - one for each shared zone */}
                    {sharedZones.map((sharedZone) => {
                      const serviceZone = getServiceZone(
                        service,
                        sharedZone.label
                      );
                      const isLinked = serviceZone !== null;

                      return (
                        <div
                          key={sharedZone.label}
                          className="w-32 border-r border-border flex-shrink-0 relative"
                        >
                          <EditableCell
                            value={serviceZone?.rate ?? null}
                            onSave={(val) =>
                              handleCellSave(
                                virtualRow.index,
                                sharedZone.label,
                                val
                              )
                            }
                            isLinked={isLinked}
                            onLink={() =>
                              handleLinkZone(virtualRow.index, sharedZone)
                            }
                            onUnlink={
                              isLinked
                                ? () =>
                                    handleUnlinkZone(
                                      virtualRow.index,
                                      sharedZone.label
                                    )
                                : undefined
                            }
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

      {/* Add Zone Button at Bottom */}
      {services.length > 0 && (
        <div className="mt-4 flex justify-center p-2">
          <Button onClick={onAddZone} variant="outline">
            <PlusIcon className="h-4 w-4 mr-2" />
            Add Zone
          </Button>
        </div>
      )}
    </div>
  );
}

export default RateSheetTable;
