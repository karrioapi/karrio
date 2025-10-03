import { Dialog, DialogContent, DialogDescription, DialogFooter, DialogHeader, DialogTitle } from "./ui/dialog";
import { Button } from "./ui/button";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "./ui/select";
import React from "react";
import { CarrierImage } from "@karrio/ui/core/components/carrier-image";

interface LinkRateSheetDialogProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  connection: { id: string; carrier_name: string; display_name?: string };
  rateSheets: Array<{ id: string; name: string; carrier_name: string }>;
  onLink: (opts: { connection_id: string; rate_sheet_id: string }) => Promise<any>;
  isLoading?: boolean;
  // Optional extras to improve UX
  linkedRateSheets?: Array<{ id: string; name: string; carrier_name: string }>;
  onEditRateSheet?: (id: string) => void;
  onCreateNew?: () => void;
}

export function LinkRateSheetDialog({
  open,
  onOpenChange,
  connection,
  rateSheets,
  onLink,
  isLoading,
  linkedRateSheets = [],
  onEditRateSheet,
  onCreateNew,
}: LinkRateSheetDialogProps) {
  const [selected, setSelected] = React.useState<string>("");

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="max-w-2xl max-h-[90vh] p-0 flex flex-col">
        {/* Sticky Header */}
        <DialogHeader className="px-4 py-3 border-b sticky top-0 bg-background z-10">
          <DialogTitle>Link an existing rate sheet</DialogTitle>
          <DialogDescription>
            Select a compatible rate sheet to link to this connection. You can also edit already linked ones or create a new rate sheet.
          </DialogDescription>
        </DialogHeader>

        {/* Scrollable Body */}
        <div className="flex-1 overflow-y-auto px-4 py-3 space-y-5">
          {/* Connection summary */}
          <div className="flex items-center gap-3 p-3 border rounded-lg bg-gray-50">
            <CarrierImage carrier_name={connection.carrier_name} width={32} height={32} className="rounded" />
            <div className="min-w-0">
              <div className="font-medium text-sm text-gray-900 truncate">{connection.display_name || connection.carrier_name}</div>
              <div className="text-xs text-gray-500">Carrier: {connection.carrier_name}</div>
            </div>
          </div>

          {/* Already linked list */}
          {linkedRateSheets.length > 0 && (
            <div className="space-y-2">
              <div className="text-sm font-medium text-gray-900">Already linked</div>
              <div className="space-y-2">
                {linkedRateSheets.map((rs) => (
                  <div key={rs.id} className="flex items-center justify-between p-3 border rounded-lg bg-white">
                    <div className="min-w-0">
                      <div className="text-sm font-medium text-gray-900 truncate">{rs.name}</div>
                      <div className="text-xs text-gray-500 truncate">{rs.carrier_name}</div>
                    </div>
                    {onEditRateSheet && (
                      <Button size="sm" variant="outline" onClick={() => onEditRateSheet(rs.id)}>
                        Edit
                      </Button>
                    )}
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Picker */}
          <div className="space-y-2">
            <div className="text-sm font-medium text-gray-900">Link another rate sheet</div>
            <Select value={selected} onValueChange={setSelected}>
              <SelectTrigger>
                <SelectValue placeholder="Select a rate sheet" />
              </SelectTrigger>
              <SelectContent>
                {rateSheets.map((rs) => (
                  <SelectItem key={rs.id} value={rs.id}>
                    {rs.name} <span className="text-gray-500">({rs.carrier_name})</span>
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
            {onCreateNew && (
              <div className="text-xs text-gray-600">
                Can't find a suitable rate sheet?{' '}
                <button
                  type="button"
                  className="text-blue-600 hover:underline"
                  onClick={onCreateNew}
                >
                  Create a new one
                </button>
              </div>
            )}
          </div>
        </div>

        {/* Sticky Footer */}
        <DialogFooter className="px-4 py-3 border-t sticky bottom-0 bg-background">
          <Button variant="outline" onClick={() => onOpenChange(false)}>
            Cancel
          </Button>
          <Button
            disabled={!selected || !!isLoading}
            onClick={() => onLink({ connection_id: connection.id, rate_sheet_id: selected })}
          >
            {isLoading ? 'Linking…' : 'Link rate sheet'}
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}
