import { Dialog, DialogContent, DialogHeader, DialogTitle } from "./ui/dialog";
import { Button } from "./ui/button";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "./ui/select";
import { Input } from "./ui/input";
import { X } from "lucide-react";
import React from "react";

interface LinkRateSheetDialogProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  connection: { id: string; carrier_name: string; display_name?: string };
  rateSheets: Array<{ id: string; name: string; carrier_name: string }>;
  onLink: (opts: { connection_id: string; rate_sheet_id: string }) => Promise<any>;
  isLoading?: boolean;
}

export function LinkRateSheetDialog({
  open,
  onOpenChange,
  connection,
  rateSheets,
  onLink,
  isLoading,
}: LinkRateSheetDialogProps) {
  const [selected, setSelected] = React.useState<string>("");

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>Link to existing rate sheet</DialogTitle>
        </DialogHeader>
        <div className="space-y-4">
          <div className="text-sm text-gray-600">
            Connection: <strong>{connection.display_name || connection.carrier_name}</strong>
          </div>
          <div>
            <Select value={selected} onValueChange={setSelected}>
              <SelectTrigger>
                <SelectValue placeholder="Select a rate sheet" />
              </SelectTrigger>
              <SelectContent>
                {rateSheets.map(rs => (
                  <SelectItem key={rs.id} value={rs.id}>
                    {rs.name} <span className="text-gray-500">({rs.carrier_name})</span>
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>
          <div className="flex justify-end gap-2">
            <Button variant="outline" onClick={() => onOpenChange(false)}>Cancel</Button>
            <Button
              disabled={!selected || isLoading}
              onClick={() => onLink({ connection_id: connection.id, rate_sheet_id: selected })}
            >
              {isLoading ? 'Linking…' : 'Link rate sheet'}
            </Button>
          </div>
        </div>
      </DialogContent>
    </Dialog>
  );
}
