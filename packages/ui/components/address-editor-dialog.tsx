import React, { useState } from "react";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogFooter,
} from "@karrio/ui/components/ui/dialog";
import { AddressType, ShipmentType } from "@karrio/types";
import { AddressForm } from "@karrio/ui/components/address-form";
import { Button } from "@karrio/ui/components/ui/button";
import { COUNTRY_WITH_POSTAL_CODE, isEqual } from "@karrio/lib";
import { useAPIMetadata } from "@karrio/hooks/api-metadata";

export interface AddressEditorDialogProps {
  header?: string;
  shipment?: ShipmentType;
  address: AddressType | ShipmentType["recipient"] | ShipmentType["shipper"];
  onSubmit: (address: AddressType) => Promise<any>;
  trigger: React.ReactElement;
}

export const AddressEditorDialog = ({
  trigger,
  header,
  shipment,
  address,
  onSubmit,
}: AddressEditorDialogProps): JSX.Element => {
  const { references } = useAPIMetadata();
  const [isOpen, setIsOpen] = useState(false);
  const [currentAddress, setCurrentAddress] = useState<Partial<AddressType>>(address || {});
  const [isSubmitting, setIsSubmitting] = useState(false);
  const formRef = React.useRef<any>(null);

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

  const handleFooterSubmit = async () => {
    if (formRef.current) {
      setIsSubmitting(true);
      try {
        await formRef.current.submit();
      } finally {
        setIsSubmitting(false);
      }
    }
  };

  const handleChange = (updatedAddress: Partial<AddressType>) => {
    setCurrentAddress(updatedAddress);
  };

  // Original validation logic from address form
  const isPostalRequired = COUNTRY_WITH_POSTAL_CODE.includes(currentAddress.country_code || "");
  const isStateRequired = Object.keys(references.states || {}).includes(currentAddress.country_code || "");
  
  const missingRequired = !currentAddress.person_name || !currentAddress.country_code || !currentAddress.address_line1 || !currentAddress.city || (isPostalRequired && !currentAddress.postal_code) || (isStateRequired && !currentAddress.state_code);
  
  // Allow saving if there are changes OR if address has meaningful content (for new addresses)
  const hasChanges = !isEqual(address, currentAddress) || (
    currentAddress.person_name || currentAddress.country_code || currentAddress.address_line1 || currentAddress.city
  );

  // Enhanced postal code validation (copied from address form)
  const validatePostalCode = (postal: string, country: string) => {
    if (!postal || !isPostalRequired) return true;

    const patterns: Record<string, RegExp> = {
      US: /^\d{5}(-\d{4})?$/,
      CA: /^[A-Za-z]\d[A-Za-z] ?\d[A-Za-z]\d$/,
      GB: /^[A-Z]{1,2}\d[A-Z\d]? ?\d[A-Z]{2}$/i,
      DE: /^\d{5}$/,
      FR: /^\d{5}$/,
      AU: /^\d{4}$/,
      JP: /^\d{3}-\d{4}$/,
    };

    return patterns[country]?.test(postal) ?? true;
  };

  const isPostalValid = validatePostalCode(currentAddress.postal_code || "", currentAddress.country_code || "");

  return (
    <>
      {React.cloneElement(trigger, {
        onClick: () => setIsOpen(true),
      })}
      
      <Dialog open={isOpen} onOpenChange={setIsOpen}>
        <DialogContent className="max-w-3xl max-h-[95vh] flex flex-col">
          <DialogHeader className="sticky top-0 bg-white z-10 pb-4 border-b">
            <DialogTitle className="text-lg font-semibold">
              {header || "Edit address"}
            </DialogTitle>
          </DialogHeader>
          
          <div className="flex-1 overflow-y-auto mt-4 pb-6 px-4">
            <AddressForm
              ref={formRef}
              value={currentAddress}
              onChange={handleChange}
              onSubmit={handleSubmit}
              showSubmitButton={false}
            />
          </div>

          {/* Sticky Footer */}
          <DialogFooter className="px-4 py-3 border-t sticky bottom-0 bg-background">
            <Button 
              type="button" 
              variant="outline" 
              onClick={() => setIsOpen(false)}
            >
              Cancel
            </Button>
            <Button
              type="button"
              onClick={handleFooterSubmit}
              disabled={isSubmitting || !hasChanges || missingRequired || (Boolean(currentAddress.postal_code) && !isPostalValid)}
            >
              {isSubmitting ? "Saving..." : "Save Address"}
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </>
  );
};

AddressEditorDialog.displayName = "AddressEditorDialog";
