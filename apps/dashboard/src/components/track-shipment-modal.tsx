import { SystemConnectionType, useSystemConnections } from '@/context/system-connection';
import { CarrierConnectionType, useCarrierConnections } from '@/context/user-connection';
import React, { useContext, useEffect, useState } from 'react';
import { errorToMessages, removeUrlParam } from '@/lib/helper';
import SelectField from '@/components/generic/select-field';
import { useTrackerMutation } from '@/context/tracker';
import InputField from '@/components/generic/input-field';
import Notifier, { Notify } from '@/components/notifier';
import { NotificationType } from '@/lib/types';
import { Loading } from '@/components/loader';
import { useAppMode } from '@/context/app-mode';
import { useAPIMetadata } from '@/context/api-metadata';

type Connection = CarrierConnectionType | SystemConnectionType;
type OperationType = {
  onChange?: () => void;
};
interface TrackerModalInterface {
  addTracker: (operation?: OperationType) => void;
}

export const TrackerModalContext = React.createContext<TrackerModalInterface>({} as TrackerModalInterface);

const TrackerModalProvider: React.FC<{}> = ({ children }) => {
  const { testMode } = useAppMode();
  const mutation = useTrackerMutation();
  const { notify } = useContext(Notify);
  const { references } = useAPIMetadata();
  const { loading, setLoading } = useContext(Loading);
  const { query: { data: userQuery, ...user } } = useCarrierConnections();
  const { query: { data: systemQuery, ...system } } = useSystemConnections();
  const [isActive, setIsActive] = useState<boolean>(false);
  const [key, setKey] = useState<string>(`tracker-${Date.now()}`);
  const [carrier, setCarrier] = useState<Connection>();
  const [trackingNumber, setTrackingNumber] = useState<string>('');
  const [operation, setOperation] = useState<OperationType>({} as OperationType);
  const [carrierList, setCarrierList] = useState<Connection[]>([]);

  const addTracker = (operation?: OperationType) => {
    operation && setOperation(operation);
    setIsActive(true);
  };
  const close = ({ updated }: any | { updated?: boolean }) => {
    setIsActive(false);
    setCarrier(undefined);
    setTrackingNumber('');
    setKey(`tracker-${Date.now()}`);
    (updated && operation?.onChange) && operation.onChange();
    removeUrlParam('modal');
  };
  const create = async (evt: React.FormEvent<HTMLFormElement>) => {
    evt.preventDefault();
    setLoading(true);
    try {
      await mutation.createTracker.mutateAsync({
        tracking_number: trackingNumber,
        carrier_name: carrier!.carrier_name,
      });
      notify({ type: NotificationType.success, message: 'Tracker successfully added!' });
      close({ updated: true });
    } catch (error: any) {
      notify({ type: NotificationType.error, message: errorToMessages(error) });
    }
    setLoading(false);
  };
  const updateCarrier = (carrierId: string) => {
    const carrier = carrierList.find(carrier => carrier?.carrier_id === carrierId);
    setCarrier(carrier);
  };

  useEffect(() => {
    const connections = [
      ...(userQuery?.user_connections || []),
      ...(systemQuery?.system_connections || []),
    ].filter(c => (
      c.active &&
      c.carrier_name in references.carriers &&
      c.carrier_name !== 'generic' &&
      (c as any).enabled !== false &&
      c.capabilities.includes('tracking')
    ));

    setCarrierList(connections);
  }, [userQuery?.user_connections, systemQuery?.system_connections]);

  return (
    <>
      <TrackerModalContext.Provider value={{ addTracker }}>
        {children}
      </TrackerModalContext.Provider>

      <Notifier>
        <div className={`modal ${isActive ? "is-active" : ""}`} key={key}>
          <div className="modal-background"></div>
          {isActive && <form className="modal-card" onSubmit={create}>
            <section className="modal-card-body modal-form">
              <div className="form-floating-header p-4">
                <span className="has-text-weight-bold is-size-6">Track package</span>
              </div>
              <div className="p-3 my-4"></div>

              <InputField label="Tracking Number" defaultValue="" onChange={e => setTrackingNumber(e.target.value)} fieldClass="mt-6" required />

              {carrierList.length > 0 &&
                <SelectField label="Carrier" onChange={e => updateCarrier(e.target.value)} className="is-fullwidth" required>
                  <option value="">Select a carrier</option>

                  {carrierList
                    .map((carrier, index) => (
                      <option key={index} value={carrier.carrier_id}>
                        {`${(references.carriers as any)[carrier.carrier_name]} ${carrier.test_mode ? '(Sandbox)' : ''}`}
                      </option>
                    ))}
                </SelectField>}

              {(user.isFetched && system.isFetched && carrierList.length === 0) &&
                <div className="notification is-warning">
                  No {testMode ? 'carrier (Sandbox)' : 'carrier'} connections available to process tracking requests.
                </div>}

              <div className="p-3 my-5"></div>
              <div className="form-floating-footer has-text-centered p-1">
                <button className="button is-default m-1 is-small" onClick={close} disabled={loading}>
                  <span>Cancel</span>
                </button>
                <button className={`button is-primary ${loading ? 'is-loading' : ''} m-1 is-small`}
                  disabled={loading} type="submit">
                  <span>Submit</span>
                </button>
              </div>

            </section>
          </form>}

          <button className="modal-close is-large has-background-dark" aria-label="close" onClick={close}></button>
        </div>
      </Notifier>
    </>
  )
};

export default TrackerModalProvider;
