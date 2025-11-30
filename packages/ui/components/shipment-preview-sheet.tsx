"use client";
import { ShipmentComponent } from "@karrio/core/modules/Shipments/shipment";
import {
  Sheet,
  SheetContent,
  SheetHeader,
  SheetTitle,
  SheetDescription,
  SheetClose
} from "@karrio/ui/components/ui/sheet";
import { X } from "lucide-react";
import { useLocation } from "@karrio/hooks/location";
import React, { useState } from "react";

type ShipmentPreviewSheetContextType = {
  previewShipment: (shipmentId: string) => void;
};

interface ShipmentPreviewSheetComponent {
  children?: React.ReactNode;
}

export const ShipmentPreviewSheetContext = React.createContext<ShipmentPreviewSheetContextType>(
  {} as ShipmentPreviewSheetContextType,
);

export const ShipmentPreviewSheet = ({ children }: ShipmentPreviewSheetComponent): JSX.Element => {
  const { addUrlParam, removeUrlParam } = useLocation();
  const [isActive, setIsActive] = useState<boolean>(false);
  const [key, setKey] = useState<string>(`shipment-${Date.now()}`);
  const [shipmentId, setShipmentId] = useState<string>();

  const previewShipment = (shipmentId: string) => {
    setShipmentId(shipmentId);
    setIsActive(true);
    setKey(`shipment-${Date.now()}`);
    addUrlParam("modal", shipmentId);
  };

  const dismiss = (_?: any) => {
    setShipmentId(undefined);
    setIsActive(false);
    setKey(`shipment-${Date.now()}`);
    removeUrlParam("modal");
  };

  return (
    <>
      <ShipmentPreviewSheetContext.Provider value={{ previewShipment }}>
        {children}
      </ShipmentPreviewSheetContext.Provider>

      <Sheet open={isActive} onOpenChange={(open) => !open && dismiss()}>
        <SheetContent
          className="w-full sm:w-[800px] sm:max-w-[800px] p-0 shadow-none"
          side="right"
        >
          <div className="h-full flex flex-col">
            <SheetHeader className="sticky top-0 z-10 bg-white px-4 py-3 border-b">
              <div className="flex items-center justify-between">
                <SheetTitle className="text-lg font-semibold">
                  Shipment Preview
                </SheetTitle>
                <SheetClose className="rounded-sm opacity-70 ring-offset-background transition-opacity hover:opacity-100 focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2 disabled:pointer-events-none">
                  <X className="h-4 w-4" />
                  <span className="sr-only">Close</span>
                </SheetClose>
              </div>
            </SheetHeader>

            <div className="flex-1 overflow-y-auto px-4 py-4">
              {isActive && shipmentId && (
                <ShipmentComponent
                  key={key}
                  shipmentId={shipmentId}
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