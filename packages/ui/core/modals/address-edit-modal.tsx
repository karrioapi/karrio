"use client";
import {
  AddressTemplateType,
  AddressType,
  DEFAULT_ADDRESS_CONTENT,
  NotificationType,
} from "@karrio/types";
import { useAddressTemplateMutation } from "@karrio/hooks/address";
import { Checkbox } from "@karrio/ui/components/ui/checkbox";
import { Label } from "@karrio/ui/components/ui/label";
import { Notifier, Notify } from "../components/notifier";
import { InputField } from "@karrio/ui/components/input-field";
import { useLocation } from "@karrio/hooks/location";
import React, { useContext, useState } from "react";
import { AddressForm } from "../forms/address-form";
import { Loading } from "../components/loader";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
} from "@karrio/ui/components/ui/dialog";
import { isNone } from "@karrio/lib";

const DEFAULT_TEMPLATE_CONTENT = {
  label: "",
  is_default: false,
  address: DEFAULT_ADDRESS_CONTENT,
} as AddressTemplateType;

type OperationType = {
  addressTemplate?: AddressTemplateType;
  onConfirm?: () => Promise<any>;
};
type AddressEditContextType = {
  editAddress: (operation?: OperationType) => void;
};

export const AddressEditContext = React.createContext<AddressEditContextType>(
  {} as AddressEditContextType,
);

interface AddressEditModalComponent {
  children?: React.ReactNode;
}

export const AddressEditModal = ({
  children,
}: AddressEditModalComponent): JSX.Element => {
  const { notify } = useContext(Notify);
  const { setLoading } = useContext(Loading);
  const mutation = useAddressTemplateMutation();
  const [isNew, setIsNew] = useState<boolean>(true);
  const { addUrlParam, removeUrlParam } = useLocation();
  const [isActive, setIsActive] = useState<boolean>(false);
  const [key, setKey] = useState<string>(`address-${Date.now()}`);
  const [operation, setOperation] = useState<OperationType | undefined>();
  const [template, setTemplate] = useState<AddressTemplateType | undefined>();

  const editAddress = (operation: OperationType = {}) => {
    const template = operation.addressTemplate || DEFAULT_TEMPLATE_CONTENT;

    setOperation(operation);
    setIsNew(isNone(operation.addressTemplate));
    setTemplate({ ...template });

    setIsActive(true);
    setKey(`address-${Date.now()}`);
    addUrlParam("modal", template.id || "new");
  };
  const close = (_?: React.MouseEvent, changed?: boolean) => {
    if (isNew) setTemplate(undefined);
    if (changed && operation?.onConfirm !== undefined) operation?.onConfirm();

    setIsActive(false);
    setOperation(undefined);
    setKey(`address-${Date.now()}`);
    removeUrlParam("modal");
  };

  const handleChange = (event: React.ChangeEvent<any>) => {
    const target = event.target;
    const name = target.name;
    const value = target.type === "checkbox" ? target.checked : target.value;

    setTemplate({ ...template, [name]: value } as AddressTemplateType);
  };
  const handleSubmit = async ({
    validation,
    ...address
  }: AddressType | any) => {
    const payload = { ...template, address };

    try {
      setLoading(true);
      if (isNew) {
        await mutation.createAddressTemplate.mutateAsync(payload as any);
        notify({
          type: NotificationType.success,
          message: "Address successfully added!",
        });
      } else {
        await mutation.updateAddressTemplate.mutateAsync(payload as any);
        notify({
          type: NotificationType.success,
          message: "Address successfully updated!",
        });
      }
      setTimeout(() => close(undefined, true), 2000);
    } catch (message: any) {
      notify({ type: NotificationType.error, message });
    }
    setLoading(false);
  };

  return (
    <Notifier>
      <AddressEditContext.Provider value={{ editAddress }}>
        {children}
      </AddressEditContext.Provider>

      <Dialog open={isActive} onOpenChange={(open) => !open && close()}>
        <DialogContent className="max-w-4xl max-h-[95vh] overflow-y-auto">
          <DialogHeader>
            <DialogTitle className="text-lg font-semibold">
              Edit address
            </DialogTitle>
          </DialogHeader>

          <div className="mt-2 pb-4">
            {template !== undefined && (
              <AddressForm
                name="template"
                value={template.address}
                onSubmit={async (address) => handleSubmit(address)}
                onTemplateChange={(isUnchanged) => {
                  const defaultValue =
                    operation?.addressTemplate || DEFAULT_TEMPLATE_CONTENT;
                  return (
                    isUnchanged &&
                    template.label === defaultValue.label &&
                    template.is_default === defaultValue.is_default
                  );
                }}
              >
                <div className="w-full mb-0">
                  <InputField
                    label="label"
                    name="label"
                    onChange={handleChange}
                    defaultValue={template?.label}
                    className="h-9"
                    wrapperClass="w-full px-1 py-3"
                    fieldClass="mb-0 p-0"
                    required
                  />
                </div>
                <div className="flex items-center space-x-2 mb-4 px-2 py-3">
                  <Checkbox
                    id="is_default"
                    name="is_default"
                    onCheckedChange={(checked) => handleChange({ target: { name: 'is_default', type: 'checkbox', checked } } as any)}
                    defaultChecked={template?.is_default as boolean}
                  />
                  <Label htmlFor="is_default" className="text-sm font-normal capitalize" style={{ fontSize: ".8em" }}>
                    Set as default address
                  </Label>
                </div>
              </AddressForm>
            )}
          </div>
        </DialogContent>
      </Dialog>
    </Notifier>
  );
};

export function useAddressEditModal() {
  return React.useContext(AddressEditContext);
}
