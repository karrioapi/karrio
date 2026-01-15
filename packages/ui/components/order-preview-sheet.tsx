"use client";
import { OrderComponent } from "@karrio/core/modules/Orders/order";
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

type OrderPreviewSheetContextType = {
  previewOrder: (orderId: string) => void;
};

interface OrderPreviewSheetComponent {
  children?: React.ReactNode;
}

export const OrderPreviewSheetContext = React.createContext<OrderPreviewSheetContextType>(
  {} as OrderPreviewSheetContextType,
);

export const OrderPreviewSheet = ({ children }: OrderPreviewSheetComponent): JSX.Element => {
  const { addUrlParam, removeUrlParam } = useLocation();
  const [isActive, setIsActive] = useState<boolean>(false);
  const [key, setKey] = useState<string>(`order-${Date.now()}`);
  const [orderId, setOrderId] = useState<string>();

  const previewOrder = (orderId: string) => {
    setOrderId(orderId);
    setIsActive(true);
    setKey(`order-${Date.now()}`);
    addUrlParam("modal", orderId);
  };

  const dismiss = (_?: any) => {
    setOrderId(undefined);
    setIsActive(false);
    setKey(`order-${Date.now()}`);
    removeUrlParam("modal");
  };

  return (
    <>
      <OrderPreviewSheetContext.Provider value={{ previewOrder }}>
        {children}
      </OrderPreviewSheetContext.Provider>

      <Sheet open={isActive} onOpenChange={(open) => !open && dismiss()}>
        <SheetContent
          className="w-full sm:w-[800px] sm:max-w-[800px] p-0 shadow-none"
          side="right"
        >
          <div className="h-full flex flex-col">
            <SheetHeader className="sticky top-0 z-10 bg-white px-4 py-3 border-b">
              <div className="flex items-center justify-between">
                <SheetTitle className="text-lg font-semibold">
                  Order Preview
                </SheetTitle>
                <SheetClose className="rounded-sm opacity-70 ring-offset-background transition-opacity hover:opacity-100 focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2 disabled:pointer-events-none">
                  <X className="h-4 w-4" />
                  <span className="sr-only">Close</span>
                </SheetClose>
              </div>
            </SheetHeader>

            <div className="flex-1 overflow-y-auto px-4 py-4">
              {isActive && orderId && (
                <OrderComponent
                  key={key}
                  orderId={orderId}
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
