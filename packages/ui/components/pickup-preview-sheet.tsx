"use client";
import { PickupComponent } from "@karrio/core/modules/Pickups/pickup";
import {
  Sheet,
  SheetContent,
  SheetHeader,
  SheetTitle,
  SheetClose
} from "@karrio/ui/components/ui/sheet";
import { X } from "lucide-react";
import { useLocation } from "@karrio/hooks/location";
import React, { useState } from "react";

type PickupPreviewSheetContextType = {
  previewPickup: (pickupId: string) => void;
};

interface PickupPreviewSheetComponent {
  children?: React.ReactNode;
}

export const PickupPreviewSheetContext = React.createContext<PickupPreviewSheetContextType>(
  {} as PickupPreviewSheetContextType,
);

export const PickupPreviewSheet = ({ children }: PickupPreviewSheetComponent): JSX.Element => {
  const { addUrlParam, removeUrlParam } = useLocation();
  const [isActive, setIsActive] = useState<boolean>(false);
  const [key, setKey] = useState<string>(`pickup-${Date.now()}`);
  const [pickupId, setPickupId] = useState<string>();

  const previewPickup = (pickupId: string) => {
    setPickupId(pickupId);
    setIsActive(true);
    setKey(`pickup-${Date.now()}`);
    addUrlParam("modal", pickupId);
  };

  const dismiss = (_?: any) => {
    setPickupId(undefined);
    setIsActive(false);
    setKey(`pickup-${Date.now()}`);
    removeUrlParam("modal");
  };

  return (
    <>
      <PickupPreviewSheetContext.Provider value={{ previewPickup }}>
        {children}
      </PickupPreviewSheetContext.Provider>

      <Sheet open={isActive} onOpenChange={(open) => !open && dismiss()}>
        <SheetContent
          className="w-full sm:w-[800px] sm:max-w-[800px] p-0 shadow-none"
          side="right"
        >
          <div className="h-full flex flex-col">
            <SheetHeader className="sticky top-0 z-10 bg-white px-4 py-3 border-b">
              <div className="flex items-center justify-between">
                <SheetTitle className="text-lg font-semibold">
                  Pickup Preview
                </SheetTitle>
                <SheetClose className="rounded-sm opacity-70 ring-offset-background transition-opacity hover:opacity-100 focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2 disabled:pointer-events-none">
                  <X className="h-4 w-4" />
                  <span className="sr-only">Close</span>
                </SheetClose>
              </div>
            </SheetHeader>

            <div className="flex-1 overflow-y-auto px-4 py-4">
              {isActive && pickupId && (
                <PickupComponent
                  key={key}
                  pickupId={pickupId}
                  isPreview={true}
                  isSheet={true}
                />
              )}
            </div>
          </div>
        </SheetContent>
      </Sheet>
    </>
  );
};
