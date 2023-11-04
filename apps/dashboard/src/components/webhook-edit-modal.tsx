import React, { useContext, useReducer, useState } from 'react';
import { NotificationType, EVENT_TYPES, WebhookType } from '@/lib/types';
import { Notify } from '@/components/notifier';
import InputField from '@/components/generic/input-field';
import TextAreaField from '@/components/generic/textarea-field';
import CheckBoxField from '@/components/generic/checkbox-field';
import { deepEqual, isNone, useLocation } from '@/lib/helper';
import { Loading } from '@/components/loader';
import { useWebhookMutation } from '@/context/webhook';

type OperationType = {
  webhook?: WebhookType;
  onConfirm?: () => Promise<any>;
};
type WebhookEditContextType = {
  editWebhook: (operation?: OperationType) => void,
};
const WebhookModalContext = React.createContext<WebhookEditContextType>({} as WebhookEditContextType);

type stateValue = string | boolean | string[] | Partial<WebhookType>;
const DEFAULT_STATE = {
  test_mode: false,
};

function reducer(state: any, { name, value }: { name: string, value: stateValue }) {
  switch (name) {
    case 'partial':
      return { ...(value as WebhookType) };
    default:
      return { ...state, [name]: value }
  }
}

const WebhookEditModal: React.FC = ({ children }) => {
  const mutation = useWebhookMutation();
  const { notify } = useContext(Notify);
  const { setLoading, loading } = useContext(Loading);
  const { addUrlParam, removeUrlParam } = useLocation();
  const [isActive, setIsActive] = useState<boolean>(false);
  const [key, setKey] = useState<string>(`webhook-${Date.now()}`);
  const [isNew, setIsNew] = useState<boolean>(true);
  const [payload, dispatch] = useReducer(reducer, DEFAULT_STATE, () => DEFAULT_STATE);
  const [operation, setOperation] = useState<OperationType | undefined>();

  const editWebhook = (operation?: OperationType) => {
    const data = operation?.webhook || DEFAULT_STATE;

    setIsActive(true);
    setOperation(operation);
    setKey(`webhook-${Date.now()}`);
    setIsNew(isNone(operation?.webhook));
    dispatch({ name: 'partial', value: data });
    addUrlParam('modal', operation?.webhook?.id || 'new');
  };
  const close = (_?: React.MouseEvent) => {
    if (isNew) dispatch({ name: 'partial', value: DEFAULT_STATE });
    setIsActive(false);
    setOperation(undefined);
    setKey(`webhook-${Date.now()}`);
    removeUrlParam('modal');
  };

  const handleChange = (event: React.ChangeEvent<any>) => {
    const target = event.target;
    let name: string = target.name;
    let value: stateValue = target.type === 'checkbox' ? target.checked : target.value;

    if (target.multiple === true) {
      value = Array.from(target.selectedOptions).map((o: any) => o.value)
    }

    dispatch({ name, value });
  };
  const handleSubmit = async (evt: React.FormEvent<HTMLFormElement>) => {
    evt.preventDefault();
    setLoading(true);
    try {
      if (isNew) {
        await mutation.createWebhook.mutateAsync(payload);
      } else {
        await mutation.updateWebhook.mutateAsync(payload);
      }
      notify({
        type: NotificationType.success,
        message: `Webhook ${isNew ? 'added' : 'updated'} successfully`
      });
      setTimeout(() => close(), 2000);
      operation?.onConfirm && operation.onConfirm();
    } catch (message: any) {
      notify({ type: NotificationType.error, message });
    }
    setLoading(false);
  };

  return (
    <>
      <WebhookModalContext.Provider value={{ editWebhook }}>
        {children}
      </WebhookModalContext.Provider>

      <div className={`modal ${isActive ? "is-active" : ""}`} key={key}>
        <div className="modal-background"></div>
        <form className="modal-card" onSubmit={handleSubmit}>
          <section className="modal-card-body modal-form">
            <div className="form-floating-header p-4">
              <span className="has-text-weight-bold is-size-6">{isNew ? 'Add ' : 'Update '} a webhook endpoint</span>
            </div>
            <div className="p-3 my-4"></div>

            <InputField label="Endpoint URL" name="url" value={payload?.url} onChange={handleChange} className="is-small" required />

            <TextAreaField label="Description" name="description" value={payload?.description as string} onChange={handleChange} className="is-small" />

            <div className="field mb-2">
              <label className="label is-capitalized" style={{ fontSize: ".8em" }}>
                <span>Events</span>
                <span className="icon is-small has-text-danger small-icon"><i className="fas fa-asterisk"></i></span>
              </label>

              <div className="control">
                <div className="select is-multiple is-fullwidth">
                  <select name="enabled_events" defaultValue={payload?.enabled_events} onChange={handleChange} size={6} multiple required>
                    {EVENT_TYPES.map(event => <option key={event} value={event}>{event}</option>)}
                  </select>
                </div>
              </div>
            </div>

            {!isNew && <>
              <hr className="my-4" style={{ height: '1px' }} />

              <InputField
                label="Secret"
                name="secret"
                value={payload?.secret}
                className="is-small"
                readOnly
                disabled
              />
            </>}

            <div className="p-3 my-5"></div>
            <div className="form-floating-footer has-text-centered p-1">
              <button className="button is-default m-1 is-small" onClick={close} disabled={loading}>
                <span>Cancel</span>
              </button>
              <button className={`button is-primary ${loading ? 'is-loading' : ''} m-1 is-small`}
                disabled={deepEqual(payload, operation?.webhook) || loading}
                type="submit">
                <span>Submit</span>
              </button>
            </div>

          </section>
        </form>
        <button className="modal-close is-large has-background-dark" aria-label="close" onClick={close}></button>
      </div>
    </>
  )
};

export function useWebhookModal() {
  return useContext(WebhookModalContext);
}


export default WebhookEditModal;
