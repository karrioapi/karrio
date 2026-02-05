"use client";

import { PlusIcon } from "@radix-ui/react-icons";
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "@karrio/ui/components/ui/popover";
import type { ServiceLevelWithZones } from "@karrio/ui/components/rate-sheet-editor";

interface ServicePreset {
  code: string;
  name: string;
}

interface AddServicePopoverProps {
  services: ServiceLevelWithZones[];
  onAddService: () => void;
  servicePresets?: ServicePreset[];
  onAddServiceFromPreset?: (serviceCode: string) => void;
  onCloneService?: (service: ServiceLevelWithZones) => void;
  align?: "start" | "end" | "center";
  iconOnly?: boolean;
}

export function AddServicePopover({
  services,
  onAddService,
  servicePresets,
  onAddServiceFromPreset,
  onCloneService,
  align = "end",
  iconOnly = false,
}: AddServicePopoverProps) {
  return (
    <Popover>
      <PopoverTrigger asChild>
        {iconOnly ? (
          <button
            className="p-1.5 text-muted-foreground hover:text-primary hover:bg-accent rounded-md transition-colors"
            title="Add service"
          >
            <PlusIcon className="h-4 w-4" />
          </button>
        ) : (
          <button className="inline-flex items-center gap-2 px-4 py-2 text-sm font-medium text-primary-foreground bg-primary hover:bg-primary/90 rounded-md transition-colors">
            <PlusIcon className="h-4 w-4" />
            Add Service
          </button>
        )}
      </PopoverTrigger>
      <PopoverContent align={align} className="w-56 p-2" sideOffset={8}>
        <div className="space-y-1">
          <p className="text-xs font-medium text-muted-foreground px-2 py-1">
            Add service
          </p>

          {servicePresets && servicePresets.length > 0 && onAddServiceFromPreset && (
            <>
              <div className="max-h-48 overflow-y-auto space-y-0.5">
                {servicePresets.map((preset) => (
                  <button
                    key={preset.code}
                    onClick={() => onAddServiceFromPreset(preset.code)}
                    className="w-full text-left px-2 py-1.5 text-sm rounded-md hover:bg-accent transition-colors truncate"
                    title={preset.name}
                  >
                    {preset.name || preset.code}
                  </button>
                ))}
              </div>
              <div className="border-t border-border my-1" />
            </>
          )}

          {services.length > 0 && onCloneService && (
            <>
              <p className="text-xs text-muted-foreground px-2 py-0.5">
                Clone existing
              </p>
              <div className="max-h-32 overflow-y-auto space-y-0.5">
                {services.map((service) => (
                  <button
                    key={service.id}
                    onClick={() => onCloneService(service)}
                    className="w-full text-left px-2 py-1.5 text-sm rounded-md hover:bg-accent transition-colors truncate text-muted-foreground"
                    title={`Clone ${service.service_name}`}
                  >
                    {service.service_name || service.service_code}
                  </button>
                ))}
              </div>
              <div className="border-t border-border my-1" />
            </>
          )}

          <button
            onClick={onAddService}
            className="w-full text-left px-2 py-1.5 text-sm rounded-md hover:bg-accent transition-colors flex items-center gap-1.5 text-primary font-medium"
          >
            <PlusIcon className="h-3.5 w-3.5" />
            Create new service
          </button>
        </div>
      </PopoverContent>
    </Popover>
  );
}
