import React, { useState } from "react";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
} from "@karrio/ui/components/ui/dialog";
import { AddressType, ShipmentType } from "@karrio/types";
import { AddressForm } from "@karrio/ui/components/address-form";

export interface AddressModalEditorProps {
  header?: string;
  shipment?: ShipmentType;
  address: AddressType | ShipmentType["recipient"] | ShipmentType["shipper"];
  onSubmit: (address: AddressType) => Promise<any>;
  trigger: React.ReactElement;
}

export const AddressModalEditor = ({
  trigger,
  header,
  shipment,
  address,
  onSubmit,
}: AddressModalEditorProps): JSX.Element => {
  const [isOpen, setIsOpen] = useState(false);
  const [currentAddress, setCurrentAddress] = useState<Partial<AddressType>>(address || {});

  React.useEffect(() => {
    setCurrentAddress(address || {});
  }, [address]);

  const handleSubmit = async (data: Partial<AddressType>) => {
    try {
      await onSubmit(data as AddressType);
      setIsOpen(false);
    } catch (error) {
      // Error is handled by the AddressForm component
      console.error("Address submission error:", error);
    }
  };

  const handleChange = (updatedAddress: Partial<AddressType>) => {
    setCurrentAddress(updatedAddress);
  };

  return (
    <>
      {React.cloneElement(trigger, {
        onClick: () => setIsOpen(true),
      })}
      
      <Dialog open={isOpen} onOpenChange={setIsOpen}>
        <DialogContent className="max-w-3xl max-h-[95vh] overflow-y-auto">
          <DialogHeader>
            <DialogTitle className="text-lg font-semibold">
              {header || "Edit address"}
            </DialogTitle>
          </DialogHeader>
          
          <div className="mt-4 pb-6 px-6">
            <AddressForm
              value={currentAddress}
              onChange={handleChange}
              onSubmit={handleSubmit}
              showSubmitButton={true}
              submitButtonText="Save Address"
            />
          </div>
        </DialogContent>
      </Dialog>
    </>
  );
};

AddressModalEditor.displayName = "AddressModalEditor";
