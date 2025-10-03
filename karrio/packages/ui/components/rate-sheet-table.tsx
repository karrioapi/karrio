"use client";

import { useVirtualizer } from "@tanstack/react-virtual";
import { useRateSheetCellMutation } from "@karrio/hooks/rate-sheet";
import { Button } from "@karrio/ui/components/ui/button";
import { Input } from "@karrio/ui/components/ui/input";
import { PlusIcon, TrashIcon } from "@radix-ui/react-icons";
import { debounce } from "@karrio/lib";
import React from "react";
import { cn } from "@karrio/ui/lib/utils";

interface RateSheetTableProps {
  rateSheetId: string;
  services: any[];
  editable?: boolean;
  onAddZone?: (serviceId: string) => void;
  onRemoveZone?: (serviceId: string, zoneIndex: number) => void;
  onAddService?: () => void;
  onRemoveService?: (serviceId: string) => void;
  onCellChange?: (serviceId: string, zoneId: string, field: string, value: any) => void;
  onBatchUpdate?: (data: { id: string; updates: any[] }) => Promise<any>;
}

const EditableCell = React.memo(({
  value,
  onSave,
  disabled,
  isPending,
  cellKey,
  type = 'number',
  displayAsNumber = true
}: {
  value: number | string;
  onSave: (value: string) => void;
  disabled: boolean;
  isPending: boolean;
  cellKey: string;
  type?: 'number' | 'text';
  displayAsNumber?: boolean;
}) => {
  const [isEditing, setIsEditing] = React.useState(false);
  const [editValue, setEditValue] = React.useState(value?.toString() || '');
  const [localValue, setLocalValue] = React.useState(value?.toString() || '');
  const inputRef = React.useRef<HTMLInputElement>(null);

  // Update local value when prop value changes (from successful save)
  React.useEffect(() => {
    setLocalValue(value?.toString() || '');
    if (!isEditing) {
      setEditValue(value?.toString() || '');
    }
  }, [value, isEditing]);

  React.useEffect(() => {
    if (isEditing && inputRef.current) {
      inputRef.current.focus();
      inputRef.current.select();
    }
  }, [isEditing]);

  const handleSave = () => {
    if (editValue !== localValue) {
      onSave(editValue);
      setLocalValue(editValue); // Optimistically update local value
    }
    setIsEditing(false);
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter') {
      handleSave();
    } else if (e.key === 'Escape') {
      setEditValue(localValue);
      setIsEditing(false);
    }
  };

  if (isEditing) {
    return (
      <Input
        ref={inputRef}
        type={type}
        step={type === 'number' ? "0.01" : undefined}
        value={editValue}
        onChange={(e) => setEditValue(e.target.value)}
        onBlur={handleSave}
        onKeyDown={handleKeyDown}
        disabled={disabled}
        className="h-8 text-center w-full border-blue-500 bg-blue-50"
      />
    );
  }

  return (
    <div
      className={cn(
        "h-8 w-full flex items-center justify-center cursor-pointer rounded px-2",
        "hover:bg-gray-100 transition-colors",
        isPending && "bg-yellow-50 border border-yellow-200",
        disabled && "cursor-not-allowed opacity-50"
      )}
      onClick={() => !disabled && setIsEditing(true)}
      title={disabled ? "Read only" : "Click to edit"}
    >
      <span className="text-sm font-mono">
        {localValue !== '' && localValue !== undefined
          ? (displayAsNumber && !isNaN(Number(localValue)) ? Number(localValue).toFixed(2) : localValue)
          : ''}
      </span>
    </div>
  );
});

EditableCell.displayName = 'EditableCell';

const ServiceRow = React.memo(({
  service,
  maxZones,
  editable,
  onCellChange,
  onAddZone,
  onRemoveZone,
  onRemoveService,
  pendingUpdates,
  style
}: {
  service: any;
  maxZones: number;
  editable: boolean;
  onCellChange: (serviceId: string, zoneId: string, field: string, value: any) => void;
  onAddZone?: (serviceId: string) => void;
  onRemoveZone?: (serviceId: string, zoneIndex: number) => void;
  onRemoveService?: (serviceId: string) => void;
  pendingUpdates: any[];
  style?: React.CSSProperties;
}) => {
  return (
    <div
      className="flex border-b hover:bg-gray-50/50 min-h-[48px]"
      style={style}
    >
      {/* Service Column (sticky left) */}
      <div
        className="sticky left-0 z-20 bg-white border-r flex items-center"
        style={{
          minWidth: '200px',
          maxWidth: '200px',
          position: 'sticky',
          left: 0
        }}
      >
        <div className="flex items-center justify-between p-2 w-full">
          <div className="min-w-0 flex-1">
            <div className="font-semibold text-sm truncate">{service.service_name}</div>
            <div className="text-xs text-muted-foreground truncate">{service.service_code}</div>
          </div>
          {editable && onRemoveService && (
            <Button
              size="sm"
              variant="ghost"
              onClick={() => onRemoveService(service.id)}
              title="Remove service"
              className="h-6 w-6 p-0 ml-2"
            >
              <TrashIcon className="h-3 w-3" />
            </Button>
          )}
        </div>
      </div>

      {/* Zone Cells (rate only) */}
      {Array.from({ length: maxZones }, (_, zoneIndex) => {
        const zone = service.zones?.[zoneIndex];
        const zoneId = zone?.id || zoneIndex.toString();
        const baseKey = `${service.id}-${zoneId}`;
        const isFieldPending = (field: string) => pendingUpdates.some(u => (
          u.service_id === service.id && u.zone_id === zoneId && u.field === field
        ));

        return (
          <div
            key={zoneIndex}
            className="border-r flex items-stretch p-1 group"
            style={{
              minWidth: '120px',
              maxWidth: '120px',
              position: 'relative'
            }}
          >
            {zone ? (
              <>
                <div className="flex-1 flex items-center justify-center">
                  <EditableCell
                    value={zone.rate}
                    onSave={(value) => onCellChange(service.id, zoneId, 'rate', value)}
                    disabled={!editable}
                    isPending={isFieldPending('rate')}
                    cellKey={`${baseKey}-rate`}
                  />
                </div>
                {editable && onRemoveZone && service.zones.length > 1 && (
                  <Button
                    size="sm"
                    variant="ghost"
                    onClick={() => onRemoveZone(service.id, zoneIndex)}
                    title={`Remove zone ${zoneIndex + 1}`}
                    className="h-5 w-5 p-0 absolute right-1 top-1 opacity-0 group-hover:opacity-100 transition-opacity"
                  >
                    <TrashIcon className="h-3 w-3" />
                  </Button>
                )}
              </>
            ) : (
              <div className="h-8 bg-gray-100 rounded w-full" />
            )}
          </div>
        );
      })}

      {/* Action Column */}
      {editable && (
        <div
          className="flex items-center justify-center p-1"
          style={{
            minWidth: '100px',
            maxWidth: '100px'
          }}
        >
          <Button
            size="sm"
            variant="ghost"
            onClick={() => onAddZone?.(service.id)}
            title="Add zone to this service"
            className="h-6 w-6 p-0"
          >
            <PlusIcon className="h-3 w-3" />
          </Button>
        </div>
      )}
    </div>
  );
});

ServiceRow.displayName = 'ServiceRow';

export const RateSheetTable = ({
  rateSheetId,
  services = [],
  editable = true,
  onAddZone,
  onRemoveZone,
  onAddService,
  onRemoveService,
  onCellChange: parentOnCellChange,
  onBatchUpdate
}: RateSheetTableProps) => {
  const { batchUpdateRateSheetCells } = useRateSheetCellMutation();
  const [pendingUpdates, setPendingUpdates] = React.useState<any[]>([]);

  const parentRef = React.useRef<HTMLDivElement>(null);

  // Virtual row virtualizer for services
  const rowVirtualizer = useVirtualizer({
    count: services.length,
    getScrollElement: () => parentRef.current,
    estimateSize: () => 48,
    overscan: 5,
  });

  // Debounced batch update
  const debouncedUpdate = React.useMemo(
    () => debounce((updates: any[]) => {
      if (updates.length === 0 || rateSheetId === 'new') return;

      const exec = onBatchUpdate
        ? onBatchUpdate({ id: rateSheetId, updates })
        : batchUpdateRateSheetCells.mutateAsync({ id: rateSheetId, updates });

      Promise.resolve(exec).then(() => {
        setPendingUpdates([]);
      }).catch(() => {
        // Keep pending updates on error for retry
      });
    }, 800),
    [rateSheetId, batchUpdateRateSheetCells, onBatchUpdate]
  );

  const handleCellChange = React.useCallback((serviceId: string, zoneId: string, field: string, value: any) => {
    const numericFields = ['rate', 'min_weight', 'max_weight', 'transit_days', 'transit_time'];
    const processedValue = numericFields.includes(field)
      ? (value === '' || value === undefined || value === null ? null : (isNaN(parseFloat(value)) ? null : parseFloat(value)))
      : (value === '' ? null : value);

    // Notify parent component if callback provided
    if (parentOnCellChange) {
      parentOnCellChange(serviceId, zoneId, field, processedValue);
    }

    const updates = [
      ...pendingUpdates.filter(u => !(u.service_id === serviceId && u.zone_id === zoneId && u.field === field)),
      { service_id: serviceId, zone_id: zoneId, field, value: processedValue }
    ];
    setPendingUpdates(updates);
    debouncedUpdate(updates);
  }, [pendingUpdates, debouncedUpdate, parentOnCellChange]);

  // Calculate max zones across all services
  const maxZones = React.useMemo(() =>
    services.length > 0 ? Math.max(...services.map(s => (s.zones || []).length), 0) : 0,
    [services]
  );

  if (services.length === 0) {
    return (
      <div className="flex-1 flex items-center justify-center text-gray-500 bg-gray-50 rounded border-2 border-dashed">
        <div className="text-center p-8">
          <p className="text-lg mb-2">No services configured</p>
          <p className="text-sm mb-4">Go to the Services tab to add services first</p>
        </div>
      </div>
    );
  }

  return (
    <div className="w-full h-full flex flex-col">
      {/* Scroll container (both X and Y). Header is inside so it scrolls on X */}
      <div
        ref={parentRef}
        className="flex-1 overflow-auto bg-white"
        style={{ height: '100%', contain: 'strict' }}
      >
        <div style={{ minWidth: `${200 + (maxZones * 120) + (editable ? 100 : 0)}px` }}>
          {/* Header row: sticky only on Y; Service header sticky on X */}
          <div
            className="border-b bg-white shadow-sm flex sticky top-0 z-30"
            style={{ height: '48px' }}
          >
            <div className="sticky left-0 z-40 bg-white border-r font-semibold text-center flex items-center justify-center" style={{ minWidth: '200px', maxWidth: '200px', position: 'sticky', left: 0 }}>
              <div className="w-full px-2 text-xs uppercase text-gray-500 text-center"><span className="text-sm text-black">Service</span></div>
            </div>
            {Array.from({ length: maxZones }, (_, i) => (
              <div
                key={i}
                className="text-center bg-white font-semibold border-r flex items-center px-2"
                style={{ minWidth: '120px', maxWidth: '120px' }}
              >
                {(() => {
                  const label = services.find(s => (s.zones || [])[i])?.zones?.[i]?.label;
                  return (
                    <div className="w-full text-left">{label || `Zone ${i + 1}`}</div>
                  );
                })()}
              </div>
            ))}
            {editable && (
              <div className="text-center bg-white flex items-center justify-center" style={{ minWidth: '100px', maxWidth: '100px' }}>
                <Button size="sm" variant="ghost" onClick={() => services.forEach(s => onAddZone?.(s.id))} title="Add zone to all services" className="h-6 w-6 p-0">
                  <PlusIcon className="h-4 w-4" />
                </Button>
              </div>
            )}
          </div>

          {/* Rows area */}
          <div style={{ height: `${rowVirtualizer.getTotalSize()}px`, width: '100%', position: 'relative' }}>
            {rowVirtualizer.getVirtualItems().map((virtualRow) => {
              const service = services[virtualRow.index];

              return (
                <ServiceRow
                  key={service.id}
                  service={service}
                  maxZones={maxZones}
                  editable={editable}
                  onCellChange={handleCellChange}
                  onAddZone={onAddZone}
                  onRemoveZone={onRemoveZone}
                  onRemoveService={onRemoveService}
                  pendingUpdates={pendingUpdates}
                  style={{
                    position: 'absolute',
                    top: 0,
                    left: 0,
                    width: '100%',
                    height: `${virtualRow.size}px`,
                    transform: `translateY(${virtualRow.start}px)`,
                  }}
                />
              );
            })}
          </div>
        </div>
      </div>

      {/* Add Zone Button */}
      {editable && services.length > 0 && (
        <div className="mt-4 flex justify-center bg-white p-2">
          <Button
            onClick={() => services.forEach(s => onAddZone?.(s.id))}
            variant="outline"
          >
            <PlusIcon className="mr-2 h-4 w-4" />
            Add Zone
          </Button>
        </div>
      )}

      {/* Status indicator */}
      {pendingUpdates.length > 0 && (
        <div className="fixed bottom-4 right-4 bg-white border rounded-lg p-3 shadow-lg z-50">
          <div className="flex items-center space-x-2">
            <div className="h-2 w-2 bg-yellow-500 rounded-full animate-pulse" />
            <span className="text-sm text-gray-600">
              Saving {pendingUpdates.length} changes...
            </span>
          </div>
        </div>
      )}
    </div>
  );
};
