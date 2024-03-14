import { CurrencyCodeEnum, get_user_connections_user_connections_GenericSettingsType, CURRENCY_OPTIONS, ServiceLevelType, WEIGHT_UNITS, DIMENSION_UNITS } from '@karrio/types';
import CodeMirror, { ReactCodeMirrorRef } from '@uiw/react-codemirror';
import { Tabs, TabStateProvider } from '../components/tabs';
import { useAPIMetadata } from '@karrio/hooks/api-metadata';
import { SelectField } from '../components/select-field';
import { failsafe, isEqual, isNone } from '@karrio/lib';
import { jsonLanguage } from '@codemirror/lang-json';
import { useLoader } from '../components/loader';
import { Notifier } from '../components/notifier';
import React from 'react';
import { CheckBoxField, InputField } from '../components';


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

interface RateSheetEditModalComponent {
  children?: React.ReactNode;
}

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

export const RateSheetEditModalProvider: React.FC<RateSheetEditModalComponent> = ({ children }) => {
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
  const computeRates = (services: ServiceLevelType[]) => {
    const max = Math.max(...(services || []).map(svc => svc.zones.length));
    return [{ max, services: services || [] }];
  };
  const updateServices = (key: string) => (e: React.ChangeEvent<any>) => {
    const newValue = (services || []).map(service => ({ ...service, [key]: e.target.value }));
    editor.current!.view?.dispatch({
      changes: { from: 0, to: editor.current!.view!.state.doc.length, insert: JSON.stringify(newValue, null, 2) }
    });
    dispatch({ name: 'partial', value: newValue });
  };
  const updateSercice = (idx: number) => (event: React.ChangeEvent<any>) => {
    const target = event.target;
    const name: string = target.name;
    let value = target.type === 'checkbox' ? target.checked : target.value;
    if (target.multiple === true) {
      value = Array.from(target.selectedOptions).map((o: any) => o.value)
    }

    const newValue = (services || []).map((service, key) => key === idx ? { ...service, [name]: value } : service);
    editor.current!.view?.dispatch({
      changes: { from: 0, to: editor.current!.view!.state.doc.length, insert: JSON.stringify(newValue, null, 2) }
    });
    dispatch({ name: 'partial', value: newValue });
  };
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    operation?.onSubmit && await operation?.onSubmit(services as ServiceLevelType[]);
    // close();
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
                  name="currency"
                  label="currency"
                  onChange={updateServices('currency')}
                  value={(services || [])[0]?.currency || 'USD'}
                  className="is-small is-fullwidth"
                >
                  {CURRENCY_OPTIONS.map(unit => <option key={unit} value={unit}>{unit}</option>)}
                </SelectField>

                <SelectField
                  name="weight_unit"
                  label="weight_unit"
                  onChange={updateServices('weight_unit')}
                  value={(services || [])[0]?.weight_unit || 'KG'}
                  className="is-small is-fullwidth"
                >
                  {WEIGHT_UNITS.map(unit => <option key={unit} value={unit}>{unit}</option>)}
                </SelectField>

                <SelectField
                  name="dimension_unit"
                  label="dimension_unit"
                  onChange={updateServices('dimension_unit')}
                  value={(services || [])[0]?.dimension_unit || 'CM'}
                  className="is-small is-fullwidth"
                >
                  {DIMENSION_UNITS.map(unit => <option key={unit} value={unit}>{unit}</option>)}
                </SelectField>

                <div className="box mt-5">
                  <div className="content" style={{ fontSize: '90%' }}>
                    <p className='is-size-6'>
                      <strong>Editing your rates sheet</strong> {' '}
                      <span className='tag is-warning'>beta</span>
                    </p>
                    <p>
                      The platform propose a unified way of defining carrier service levels
                      and rates. This is a work in progress and we are looking for your
                      feedback to improve it.
                    </p>
                  </div>
                </div>

              </div>

              <div className="p-3"></div>

              <div className="column p-0 is-9">

                <TabStateProvider tabs={['RATE SHEET', 'SERVICES', 'JSON EDITOR', 'SAMPLE']} setSelectedToURL={false}>
                  <Tabs tabClass="is-size-6 has-text-weight-bold" style={{ position: 'relative' }}>
                    <div className="card" style={{ borderRadius: 0, height: '80vh', overflow: 'auto' }}>
                      <div className="table-container">
                        <table className="table is-bordered is-striped is-narrow">

                          <tbody>
                            {computeRates(services || [])
                              .map(({ max, services }) => (
                                <React.Fragment key={`svc-${new Date()}`}>
                                  <tr style={{ minWidth: '100px', position: 'sticky', top: 0, left: 0, zIndex: 1 }} className='is-selected'>
                                    <td className="is-size-7 text-ellipsis is-info" style={{ minWidth: '80px', position: 'sticky', top: 0, left: 0, zIndex: 1 }}>zones</td>
                                    {services.map(service => (
                                      <td key={service.service_code} className="is-size-7 text-ellipsis">
                                        {service.service_code}
                                      </td>
                                    ))}
                                  </tr>

                                  {(services || []).length > 0 && Array.from(Array(max).keys()).map((__, idx) => (

                                    <tr key={`${idx}-${new Date()}`}>
                                      <td className="is-size-7 is-info" style={{ minWidth: '80px', position: 'sticky', top: 0, left: 0 }}>zone {idx}</td>
                                      {services.map((service, key) => (
                                        <td key={`${key}-${new Date()}`} className="is-size-7" style={{ width: '100px', minWidth: '100px' }}>
                                          {service.zones[idx]?.rate || ''}
                                        </td>
                                      ))}
                                    </tr>

                                  ))}

                                </React.Fragment>
                              ))}
                          </tbody>

                        </table>
                      </div>
                    </div>

                    <div className="card" style={{ borderRadius: 0, height: '80vh', overflow: 'auto' }}>
                      <div className="table-container">
                        <table className="table is-bordered is-striped is-narrow">

                          <tbody>
                            <tr>
                              <td className="is-size-7">Service name</td>
                              <td className="is-size-7">Service code</td>
                              <td className="is-size-7">National</td>
                              <td className="is-size-7">International</td>
                              <td className="is-size-7">Transit days</td>
                              <td className="is-size-7">Transit time</td>
                              <td className="is-size-7">Max weight</td>
                              <td className="is-size-7">Max length</td>
                              <td className="is-size-7">Max width</td>
                              <td className="is-size-7">Max height</td>
                            </tr>

                            {(services || [])
                              .map((service, idx) => (
                                <tr key={`service-${idx}-${new Date()}`}>
                                  <td className="is-size-7 p-0">
                                    <InputField
                                      name="service_name" onChange={updateSercice(idx)} value={service.service_name || ''}
                                      className="is-small"
                                    />
                                  </td>
                                  <td className="is-size-7 p-0">
                                    <InputField
                                      name="service_code" onChange={updateSercice(idx)} value={service.service_code || ''}
                                      className="is-small"
                                    />
                                  </td>
                                  <td className="is-size-7 p-0 is-vcentered">
                                    <CheckBoxField
                                      name="domicile" onChange={updateSercice(idx)} defaultChecked={service?.domicile as boolean}
                                      fieldClass="has-text-centered"
                                    />
                                  </td>
                                  <td className="is-size-7 p-0 is-vcentered">
                                    <CheckBoxField
                                      name="international" onChange={updateSercice(idx)} defaultChecked={service?.international as boolean}
                                      fieldClass="has-text-centered"
                                    />
                                  </td>
                                  <td className="is-size-7 p-0">
                                    <InputField
                                      name="transit_days" onChange={updateSercice(idx)} value={service.transit_days || ''} type='number' step={1} min={0}
                                      className="is-small"
                                    />
                                  </td>
                                  <td className="is-size-7 p-0">
                                    <InputField
                                      name="transit_time" onChange={updateSercice(idx)} value={service.transit_time || ''} type='number' step={0.1} className="is-small"
                                    />
                                  </td>
                                  <td className="is-size-7 p-0">
                                    <InputField
                                      name="max_weight" onChange={updateSercice(idx)} value={service.max_weight || ''} type='number' step={0.1} className="is-small"
                                    />
                                  </td>
                                  <td className="is-size-7 p-0">
                                    <InputField
                                      name="max_length" onChange={updateSercice(idx)} value={service.max_length || ''} type='number' step={0.1} className="is-small"
                                    />
                                  </td>
                                  <td className="is-size-7 p-0">
                                    <InputField
                                      name="max_width" onChange={updateSercice(idx)} value={service.max_width || ''} type='number' step={0.1} className="is-small"
                                    />
                                  </td>
                                  <td className="is-size-7 p-0">
                                    <InputField
                                      name="max_length" onChange={updateSercice(idx)} value={service.max_length || ''} type='number' step={0.1} className="is-small"
                                    />
                                  </td>
                                </tr>
                              ))}
                          </tbody>

                        </table>
                      </div>
                    </div>

                    <div className="card" style={{ borderRadius: 0, overflow: 'auto' }}>
                      <CodeMirror
                        ref={editor}
                        height="76vh"
                        extensions={[jsonLanguage]}
                        value={failsafe(() => JSON.stringify(services || [], null, 2))}
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
