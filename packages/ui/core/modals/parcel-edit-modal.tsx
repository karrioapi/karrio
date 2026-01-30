"use client";
import {
  CreateParcelInput,
  DEFAULT_PARCEL_CONTENT,
  UpdateParcelInput,
} from "@karrio/types";
import { NotificationType, ParcelTemplateType } from "@karrio/types";
import { useParcelMutation } from "@karrio/hooks/parcel";
import { CheckBoxField } from "../components/checkbox-field";
import { Notifier, Notify } from "../components/notifier";
import { InputField } from "../components/input-field";
import { useLocation } from "@karrio/hooks/location";
import React, { useContext, useState } from "react";
import { ParcelForm } from "../forms/parcel-form";
import { Loading } from "../components/loader";
import { isEqual, isNone } from "@karrio/lib";

const DEFAULT_TEMPLATE_CONTENT = {
  ...DEFAULT_PARCEL_CONTENT,
  meta: { label: "", is_default: false },
} as ParcelTemplateType;

type OperationType = {
  parcelTemplate?: ParcelTemplateType;
  onConfirm?: () => Promise<any>;
};
type ParcelEditContextType = {
  editParcel: (operation?: OperationType) => void;
};

export const ParcelEditContext = React.createContext<ParcelEditContextType>(
  {} as ParcelEditContextType,
);

interface ParcelEditModalComponent {
  children?: React.ReactNode;
}

export const ParcelEditModal = ({
  children,
}: ParcelEditModalComponent): JSX.Element => {
  const { notify } = useContext(Notify);
  const mutation = useParcelMutation();
  const { setLoading, loading } = useContext(Loading);
  const { addUrlParam, removeUrlParam } = useLocation();
  const [isActive, setIsActive] = useState<boolean>(false);
  const [key, setKey] = useState<string>(`parcel-${Date.now()}`);
  const [isNew, setIsNew] = useState<boolean>(true);
  const [template, setTemplate] = useState<ParcelTemplateType | undefined>();
  const [operation, setOperation] = useState<OperationType | undefined>();
  const [isValid, setIsValid] = React.useState<boolean>(true);

  const computeDisable = (isValid: boolean, template: ParcelTemplateType) => {
    const parcelTemplate = operation?.parcelTemplate;
    const defaultMeta = parcelTemplate?.meta || { label: "", is_default: false };
    const { meta: templateMeta, ...templateData } = template || {};
    const { meta: defaultParcelMeta, ...defaultParcelData } = parcelTemplate || {};

    return (
      !isValid ||
      (templateMeta?.label === defaultMeta.label &&
        templateMeta?.is_default === defaultMeta.is_default &&
        isEqual(templateData, defaultParcelData))
    );
  };

  const editParcel = (operation?: OperationType) => {
    const parcelTemplate = operation?.parcelTemplate;
    // Use flat structure with meta field
    const template = parcelTemplate ? {
      ...parcelTemplate,
      meta: {
        label: parcelTemplate.meta?.label || "",
        is_default: parcelTemplate.meta?.is_default || false,
      },
    } : DEFAULT_TEMPLATE_CONTENT;

    setIsActive(true);
    setOperation(operation);
    setIsNew(isNone(operation?.parcelTemplate));
    setTemplate({ ...template });
    setKey(`parcel-${Date.now()}`);
    addUrlParam("modal", template.id || "new");
  };
  const close = (_?: React.MouseEvent, changed?: boolean) => {
    if (isNew) setTemplate(undefined);
    if (changed && operation?.onConfirm !== undefined) operation?.onConfirm();
    setLoading(false);
    setIsActive(false);
    setOperation(undefined);
    setKey(`parcel-${Date.now()}`);
    removeUrlParam("modal");
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      setLoading(true);
      // Extract meta and parcel data for flat structure
      const { meta, id, object_type, created_at, updated_at, created_by, ...parcelData } = template || {};
      const payload = {
        ...parcelData,
        meta,
      };

      if (isNew) {
        await mutation.createParcel.mutateAsync(payload as CreateParcelInput);
        notify({
          type: NotificationType.success,
          message: "Parcel successfully added!",
        });
      } else {
        await mutation.updateParcel.mutateAsync({ ...payload, id } as UpdateParcelInput);
        notify({
          type: NotificationType.success,
          message: "Parcel successfully updated!",
        });
      }
      setTimeout(() => close(undefined, true), 1500);
    } catch (message: any) {
      notify({ type: NotificationType.error, message });
      setLoading(false);
    }
  };

  return (
    <Notifier>
      <ParcelEditContext.Provider value={{ editParcel }}>
        {children}
      </ParcelEditContext.Provider>

      <div className={`modal ${isActive ? "is-active" : ""}`} key={key}>
        <div className="modal-background"></div>
        <div className="modal-card">
          <form
            className="modal-card-body modal-form"
            onSubmit={handleSubmit}
            onChange={(e) => setIsValid((e.target as any).checkValidity())}
          >
            <div className="form-floating-header p-4">
              <span className="has-text-weight-bold is-size-6">
                Edit parcel
              </span>
            </div>
            <div className="p-3 my-4"></div>

            {template !== undefined && (
              <ParcelForm
                value={template}
                onChange={(parcel: any) => {
                  const { meta, ...parcelData } = parcel;
                  setTemplate({ ...template, ...parcelData });
                }}
                prefixChilren={
                  <>
                    <div className="columns mb-0 px-2">
                      <InputField
                        label="label"
                        name="label"
                        onChange={(e) =>
                          setTemplate({
                            ...template,
                            meta: { ...template.meta, label: e.target.value },
                          })
                        }
                        defaultValue={template.meta?.label}
                        className="is-small"
                        wrapperClass="px-1 py-2"
                        fieldClass="column mb-0 p-0"
                        required
                      />
                    </div>
                    <div className="columns mb-1 px-1">
                      <CheckBoxField
                        name="is_default"
                        onChange={(e) =>
                          setTemplate({
                            ...template,
                            meta: { ...template.meta, is_default: e.target.checked },
                          })
                        }
                        defaultChecked={template?.meta?.is_default as boolean}
                        fieldClass="column mb-0 px-2 pt-3 pb-0"
                      >
                        <span>Set as default parcel</span>
                      </CheckBoxField>
                    </div>
                  </>
                }
              >
                <div className="p-3 my-5"></div>
                <div className="form-floating-footer has-text-centered p-1">
                  <button
                    className="button is-default m-1 is-small"
                    onClick={close}
                    disabled={loading}
                  >
                    <span>Cancel</span>
                  </button>
                  <button
                    className={`button is-primary ${loading ? "is-loading" : ""} m-1 is-small`}
                    disabled={computeDisable(isValid, template)}
                    type="submit"
                  >
                    <span>Save</span>
                  </button>
                </div>
              </ParcelForm>
            )}
          </form>
        </div>

        <button
          className="modal-close is-large has-background-dark"
          aria-label="close"
          onClick={close}
        ></button>
      </div>
    </Notifier>
  );
};

export function useParcelEditModal() {
  return React.useContext(ParcelEditContext);
}
