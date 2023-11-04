import { CurrencyCodeEnum, get_user_connections_user_connections_GenericSettingsType } from '@karrio/graphql';
import Tabs, { TabStateProvider } from '@/components/generic/tabs';
import { CURRENCY_OPTIONS, ServiceLevelType } from '@/lib/types';
import SelectField from '@/components/generic/select-field';
import InputField from '@/components/generic/input-field';
import { failsafe, isEqual, isNone } from '@/lib/helper';
import { useAPIMetadata } from '@/context/api-metadata';
import { jsonLanguage } from '@codemirror/lang-json';
import CodeMirror, { ReactCodeMirrorRef, useCodeMirror } from '@uiw/react-codemirror';
import { useLoader } from '@/components/loader';
import Notifier from '@/components/notifier';
import React from 'react';


type ConnectionType = get_user_connections_user_connections_GenericSettingsType;
type OperationType = {
  connection: ConnectionType;
  onSubmit: (services: ServiceLevelType[]) => Promise<any>;
};
type RateSheetStateContextType = {
  isActive: boolean;
  operation?: OperationType;
  editRateSheet: (operation: OperationType) => void,
};
type stateValue = string | boolean | Partial<ServiceLevelType> | ServiceLevelType[] | undefined | null;

export const RateSheetStateContext = React.createContext<RateSheetStateContextType>({} as RateSheetStateContextType);

interface RateSheetEditModalComponent { }

function reducer(state: any, { name, value }: { name: string, value: stateValue }) {
  switch (name) {
    case 'currency':
      const newValue = (state as ServiceLevelType[]).map(service => ({ ...service, currency: value }));
      return newValue as ServiceLevelType[];
    case 'partial':
    default:
      return isNone(value) ? undefined : (value as ServiceLevelType[]);
  }
}

const RateSheetEditModalProvider: React.FC<RateSheetEditModalComponent> = ({ children }) => {
  const editor = React.useRef<ReactCodeMirrorRef>(null);
  const { loading, setLoading } = useLoader();
  const { references: { service_levels } } = useAPIMetadata();
  const [isActive, setIsActive] = React.useState<boolean>(false);
  const [key, setKey] = React.useState<string>(`rates-${Date.now()}`);
  const [services, dispatch] = React.useReducer(reducer, undefined, () => []);
  const [operation, setOperation] = React.useState<OperationType | undefined>();

  const isUnChanged = (change: ServiceLevelType[]): boolean => {
    return (
      isEqual(services, operation?.connection.services || [])
    )
  }
  const editRateSheet = (operation: OperationType) => {
    const services = (operation.connection.services || []) as ServiceLevelType[];

    setIsActive(true);
    setOperation(operation);
    dispatch({ name: 'partial', value: services });
    setKey(`services-${operation.connection.id}`);
  };
  const close = (_?: React.MouseEvent) => {
    setIsActive(false);
    setOperation(undefined);
    dispatch({ name: 'partial', value: undefined });
  };
  const updateCurrency = (e: React.ChangeEvent<any>) => {
    const newValue = (services || []).map(service => ({ ...service, currency: e.target.value as CurrencyCodeEnum }));
    editor.current!.view?.dispatch({
      changes: { from: 0, to: editor.current!.view!.state.doc.length, insert: JSON.stringify(newValue, null, 2) }
    });
    dispatch({ name: 'partial', value: newValue });
  };
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    operation?.onSubmit && await operation?.onSubmit(services as ServiceLevelType[]);
    close();
  };

  return (
    <Notifier>
      <RateSheetStateContext.Provider value={{ editRateSheet, operation, isActive }}>
        {children}
      </RateSheetStateContext.Provider>

      <form onSubmit={handleSubmit} className={`modal ${isActive ? "is-active" : ""}`} key={key}>
        <div className="modal-background has-background-white"></div>
        <div className="modal-card is-large-modal">

          {operation && services !== undefined && <section className="modal-card-body p-4">

            <div className="pb-4 pt-0 is-flex is-justify-content-space-between has-background-white">
              <div className="is-vcentered">
                <button className="button is-white is-small" aria-label="close" onClick={close}>
                  <span className="icon is-large">
                    <i className="fas fa-lg fa-times"></i>
                  </span>
                </button>
                <span className="title is-6 has-text-weight-semibold p-3">Edit rate sheet</span>
              </div>
              <div>
                <button
                  type="submit"
                  className="button is-small is-success"
                  disabled={loading || isUnChanged(services)}
                >
                  Save
                </button>
              </div>
            </div>

            <hr className='my-2' style={{ height: '1px' }} />

            <div className="columns m-0">

              <div className="column px-0 pb-4">

                <SelectField
                  onChange={updateCurrency}
                  value={services[0]?.currency || computeDefaultCurrency(service_levels[operation!.connection.carrier_name] as ServiceLevelType[])}
                  name="currency"
                  className="is-small is-fullwidth"
                >
                  {CURRENCY_OPTIONS.map(unit => <option key={unit} value={unit}>{unit}</option>)}
                </SelectField>

                <div className="box mt-5">
                  <div className="content" style={{ fontSize: '90%' }}>
                    <p className='is-size-6'>
                      <strong>Editing your rates sheet</strong> {' '}
                      <span className='tag is-warning'>beta</span>
                    </p>
                    <p>
                      Karrio propose a unified way of defining carrier service levels
                      and rates. This is a work in progress and we are looking for your
                      feedback to improve it.
                    </p>
                  </div>
                </div>

              </div>

              <div className="p-3"></div>

              <div className="column p-0 is-9">

                <TabStateProvider tabs={['RATES SHEET', 'JSON EDITOR', 'SAMPLE']} defaultSelected='JSON EDITOR' disabledTabs={['RATES SHEET']} setSelectedToURL={false}>
                  <Tabs tabClass="is-size-6 has-text-weight-bold" style={{ position: 'relative' }}>
                    <div className="card" style={{ borderRadius: 0, height: '80vh' }}>
                      Service and rates management here.
                    </div>
                    <div className="card" style={{ borderRadius: 0 }}>
                      <CodeMirror
                        ref={editor}
                        height="76vh"
                        extensions={[jsonLanguage]}
                        value={failsafe(() => JSON.stringify(operation.connection.services || [], null, 2))}
                        onChange={value => failsafe(() => dispatch({ name: 'partial', value: JSON.parse(value) }))}
                      />
                    </div>
                    <div className="card" style={{ borderRadius: 0 }}>
                      <CodeMirror
                        height="76vh"
                        extensions={[jsonLanguage]}
                        value={failsafe(() => JSON.stringify(service_levels[operation!.connection.carrier_name], null, 2))}
                        editable={false}
                      />
                    </div>
                  </Tabs>
                </TabStateProvider>
              </div>

            </div>

          </section>}

        </div>
      </form>
    </Notifier>
  )
};


function computeDefaultCurrency(defaultValue: ServiceLevelType[]): CurrencyCodeEnum {
  const svc = (defaultValue || []).find(svc => !isNone(svc.currency))
  return (svc?.currency || CurrencyCodeEnum.USD) as CurrencyCodeEnum
}

export function useRateSheetModal() {
  return React.useContext(RateSheetStateContext);
}

export default RateSheetEditModalProvider;
