import { useOrganizationMutation } from '@/context/organization';
import { CreateOrganizationMutationInput } from 'karrio/graphql';
import React, { useContext, useReducer, useState } from 'react';
import Notifier, { useNotifier } from '@/components/notifier';
import InputField from '@/components/generic/input-field';
import { deepEqual, isNone } from '@/lib/helper';
import { useLoader } from '@/components/loader';
import { NotificationType } from '@/lib/types';

type OperationType = {
  onChange: (orgId: string) => Promise<any>;
};
type CreateOrganizationContextType = {
  createOrganization: (operation: OperationType) => void,
};
type stateValue = string | boolean | Partial<CreateOrganizationMutationInput> | undefined | null;

const DEFAULT_ORGANIZATION = { name: "" } as Partial<CreateOrganizationMutationInput>;

function reducer(state: Partial<CreateOrganizationMutationInput> | undefined, { name, value }: { name: string, value: stateValue }) {
  switch (name) {
    case 'partial':
      return isNone(value) ? undefined : { ...(state || {}), ...(value as CreateOrganizationMutationInput) };
    default:
      return { ...(state || {}), [name]: value }
  }
}

export const CreateOrganizationContext = React.createContext<CreateOrganizationContextType>({} as CreateOrganizationContextType);

const CreateOrganizationModalProvider: React.FC = ({ children }) => {
  const { notify } = useNotifier();
  const { loading, setLoading } = useLoader();
  const mutation = useOrganizationMutation();
  const [key, setKey] = useState<string>(`organization-${Date.now()}`);
  const [isActive, setIsActive] = useState<boolean>(false);
  const [organization, dispatch] = useReducer(reducer, undefined, () => DEFAULT_ORGANIZATION);
  const [operation, setOperation] = useState<OperationType | undefined>();

  const createOrganization = (operation: OperationType) => {
    setIsActive(true);
    setOperation(operation);
    dispatch({ name: 'partial', value: DEFAULT_ORGANIZATION });
    setKey(`organization-${Date.now()}`);
  };
  const close = (_?: React.MouseEvent | any) => {
    setIsActive(false);
    setOperation(undefined);
    dispatch({ name: 'partial', value: undefined });
    setKey(`organization-${Date.now()}`);
  };

  const handleChange = (event: React.ChangeEvent<HTMLInputElement | any>) => {
    event.preventDefault();
    const target = event.target;
    let name: string = target.name;
    let value: stateValue = target.type === 'checkbox' ? target.checked : target.value;

    dispatch({ name, value });
  };
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    try {
      const response = await mutation.createOrganization.mutateAsync(organization as any);
      notify({ type: NotificationType.success, message: 'Organization created successfully!' });
      operation?.onChange && operation?.onChange(response?.create_organization?.organization?.id as string);
      setTimeout(() => { setLoading(false); close(); }, 600);
    } catch (message: any) {
      notify({ type: NotificationType.error, message });
      setLoading(false);
    }
  };

  return (
    <Notifier>
      <CreateOrganizationContext.Provider value={{ createOrganization }}>
        {children}
      </CreateOrganizationContext.Provider>

      <div className={`modal ${isActive ? "is-active" : ""}`} key={key}>
        <div className="modal-background"></div>
        <div className="modal-card max-modal-height">

          <section className="modal-card-body modal-form">
            <div className="form-floating-header p-4">
              <span className="has-text-weight-bold is-size-6">Create a new organization</span>
            </div>
            <div className="p-3 my-4"></div>

            {organization && <>
              <div className="px-0 py-4" key={key}>

                <InputField
                  name="name"
                  label="Organization name"
                  placeholder="Company or store name"
                  onChange={handleChange}
                  defaultValue={organization.name}
                  className="is-small"
                  fieldClass="column mb-0 px-2 py-2"
                  required
                />

              </div>

              <div className="p-3 my-5"></div>
              <div className="form-floating-footer has-text-centered p-1">
                <button className="button is-default m-1 is-small" onClick={close} disabled={loading}>
                  <span>Cancel</span>
                </button>
                <button className={`button is-primary ${loading ? 'is-loading' : ''} m-1 is-small`}
                  disabled={loading || deepEqual(organization, DEFAULT_ORGANIZATION)}
                  onClick={handleSubmit}
                  type="button">
                  <span>Create organization</span>
                </button>
              </div>
            </>}
          </section>

        </div>

        <button className="modal-close is-large has-background-dark" aria-label="close" onClick={close}></button>
      </div>
    </Notifier>
  )
};

export function useCreateOrganizationModal() {
  return useContext(CreateOrganizationContext);
}

export default CreateOrganizationModalProvider;
