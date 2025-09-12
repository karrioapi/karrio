"use client";
import { ShipmentComponent } from "@karrio/core/modules/Shipments/shipment";
import { 
  Sheet, 
  SheetContent, 
  SheetHeader, 
  SheetTitle,
  SheetDescription 
} from "@karrio/ui/components/ui/sheet";
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
        <SheetContent className="w-full sm:w-[800px] sm:max-w-[800px] p-0 overflow-y-auto shadow-none" side="right">
          <div className="px-4 py-4">
            {isActive && shipmentId && (
              <ShipmentComponent 
                key={key}
                shipmentId={shipmentId} 
                isPreview={true}
                isSheet={true}
              />
            )}
          </div>
        </SheetContent>
      </Sheet>
    </>
  );
};