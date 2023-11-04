import CustomsInfoForm, { DEFAULT_CUSTOMS_CONTENT } from '@/components/form-parts/customs-info-form';
import { CreateCustomsTemplateInput, UpdateCustomsTemplateInput } from 'karrio/graphql';
import { CustomsTemplateType, CustomsType, NotificationType } from '@/lib/types';
import { useCustomsTemplateMutation } from '@/context/customs';
import CheckBoxField from '@/components/generic/checkbox-field';
import InputField from '@/components/generic/input-field';
import Notifier, { Notify } from '@/components/notifier';
import React, { useContext, useState } from 'react';
import { isNone, useLocation } from '@/lib/helper';
import { Loading } from '@/components/loader';

const DEFAULT_TEMPLATE_CONTENT = {
  label: '',
  is_default: false,
  customs: DEFAULT_CUSTOMS_CONTENT,
} as CustomsTemplateType;


type OperationType = {
  customsTemplate?: CustomsTemplateType;
  onConfirm?: () => Promise<any>;
};
type CustomsInfoEditContextType = {
  editCustomsInfo: (operation?: OperationType) => void,
};

export const CustomsInfoEditContext = React.createContext<CustomsInfoEditContextType>({} as CustomsInfoEditContextType);

interface CustomsInfoEditModalComponent { }

const CustomsInfoEditModal: React.FC<CustomsInfoEditModalComponent> = ({ children }) => {
  const { notify } = useContext(Notify);
  const { setLoading } = useContext(Loading);
  const { addUrlParam, removeUrlParam } = useLocation();
  const mutation = useCustomsTemplateMutation();
  const [isActive, setIsActive] = useState<boolean>(false);
  const [key, setKey] = useState<string>(`customs-info-${Date.now()}`);
  const [isNew, setIsNew] = useState<boolean>(true);
  const [template, setTemplate] = useState<CustomsTemplateType | undefined>();
  const [operation, setOperation] = useState<OperationType | undefined>();

  const editCustomsInfo = (operation?: OperationType) => {
    const template = operation?.customsTemplate || DEFAULT_TEMPLATE_CONTENT;

    setOperation(operation);
    setIsNew(isNone(template));
    setTemplate({ ...template });

    setIsActive(true);
    setKey(`customs-info-${Date.now()}`);
    addUrlParam('modal', template.id || 'new');
  };
  const close = (_?: React.MouseEvent, changed?: boolean) => {
    if (isNew) setTemplate(undefined);
    if (changed && operation?.onConfirm !== undefined) operation?.onConfirm();

    setIsActive(false);
    setOperation(undefined);
    setKey(`customs-info-${Date.now()}`);
    removeUrlParam('modal');
  };

  const handleChange = (event: React.ChangeEvent<any>) => {
    const target = event.target;
    const name = target.name;
    const value = target.type === 'checkbox' ? target.checked : target.value;

    setTemplate({ ...template, [name]: value } as CustomsTemplateType);
  };
  const handleSubmit = async (customs: CustomsType) => {
    const payload = { ...template, customs };

    try {
      setLoading(true);
      if (isNew) {
        await mutation.createCustomsTemplate.mutateAsync(payload as CreateCustomsTemplateInput);
        notify({ type: NotificationType.success, message: 'Customs info successfully added!' });
      }
      else {
        await mutation.updateCustomsTemplate.mutateAsync(payload as UpdateCustomsTemplateInput);
        notify({ type: NotificationType.success, message: 'Customs info successfully updated!' });
      }
      setTimeout(() => close(undefined, true), 2000);
    } catch (message: any) {
      notify({ type: NotificationType.error, message });
    }
    setLoading(false);
  };

  return (
    <Notifier>
      <CustomsInfoEditContext.Provider value={{ editCustomsInfo }}>
        {children}
      </CustomsInfoEditContext.Provider>

      <div className={`modal ${isActive ? "is-active" : ""}`} key={key}>
        <div className="modal-background"></div>
        <div className="modal-card">

          <section className="modal-card-body modal-form">
            <div className="form-floating-header p-4">
              <span className="has-text-weight-bold is-size-6">Edit customs info</span>
            </div>
            <div className="p-3 my-4"></div>

            {(template !== undefined) &&
              <CustomsInfoForm
                value={(operation?.customsTemplate?.customs || DEFAULT_CUSTOMS_CONTENT) as CustomsType}
                onSubmit={async customs => handleSubmit(customs as CustomsType)}
                onChange={(customs: any) => setTemplate({ ...template, customs } as CustomsTemplateType)}
                onTemplateChange={(isUnchanged) => {
                  const defaultValue = operation?.customsTemplate || DEFAULT_TEMPLATE_CONTENT;
                  return (
                    isUnchanged &&
                    template?.label === defaultValue.label &&
                    template?.is_default === defaultValue.is_default
                  );
                }}
                isTemplate={true}>

                <div className="columns mb-2">
                  <InputField
                    label="label"
                    name="label"
                    onChange={handleChange}
                    defaultValue={template?.label}
                    className="is-small"
                    fieldClass="column mb-0 px-2 py-2"
                    required />
                </div>

                <div className="columns mb-1">
                  <CheckBoxField
                    name="is_default"
                    onChange={handleChange}
                    defaultChecked={template?.is_default as boolean}
                    fieldClass="column mb-0 px-2 pt-3 pb-2">
                    <span>Set as default customs info</span>
                  </CheckBoxField>
                </div>

              </CustomsInfoForm>}
          </section>

        </div>

        <button className="modal-close is-large has-background-dark" aria-label="close" onClick={close}></button>
      </div>
    </Notifier>
  )
};

export default CustomsInfoEditModal;
