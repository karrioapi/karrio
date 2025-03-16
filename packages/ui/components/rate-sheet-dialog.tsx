import { Dialog, DialogContent } from "./ui/dialog";
import { Button } from "./ui/button";
import { X } from "lucide-react";
import { cn } from "@karrio/ui/lib/utils";
import { RateSheetEditor } from "./rate-sheet-editor";

interface RateSheetDialogProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  selectedRateSheet?: any;
  onSubmit: (values: any) => Promise<any>;
  isLoading?: boolean;
}

export function RateSheetDialog({
  open,
  onOpenChange,
  selectedRateSheet,
  onSubmit,
  isLoading,
}: RateSheetDialogProps) {
  if (!open) return null;

  return (
    <div className="fixed inset-0 z-50 bg-white">
      <div className="flex flex-col h-full">
        <header className="flex items-center gap-4 px-4 h-[49px] border-b bg-white sticky top-0">
          <Button
            variant="ghost"
            size="icon"
            className="h-8 w-8 -ml-2"
            onClick={() => onOpenChange(false)}
          >
            <X className="h-4 w-4" />
          </Button>

          <div className="flex items-center gap-3 flex-1">
            <h2 className="text-[15px] font-medium leading-none">
              {selectedRateSheet ? "Edit rate sheet" : "Create rate sheet"}
            </h2>
          </div>

          <div className="flex items-center gap-3">
            <Button
              variant="ghost"
              size="sm"
              className="text-sm"
            >
              Hide preview
            </Button>
            <Button
              size="sm"
              className="bg-[#635bff] hover:bg-[#635bff]/90 text-sm"
            >
              Save changes
            </Button>
          </div>
        </header>

        <div className="flex flex-1 overflow-hidden">
          <div className="w-[calc(100%-400px)] p-8 overflow-auto border-r">
            <RateSheetEditor
              sheet={selectedRateSheet}
              onSubmit={onSubmit}
              isLoading={isLoading}
            />
          </div>

          <div className="w-[400px] bg-[#f7f7f7] overflow-auto">
            <div className="p-8">
              <div className="text-sm font-medium mb-4">Preview</div>
              <div className="bg-white rounded-lg shadow-sm p-6">
                {/* Preview content will go here */}
                <div className="text-sm text-gray-500">
                  Rate sheet preview will be shown here
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
