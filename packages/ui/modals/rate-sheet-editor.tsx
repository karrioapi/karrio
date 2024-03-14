import { CreateRateSheetMutationInput, CurrencyCodeEnum, UpdateRateSheetMutationInput } from '@karrio/types/graphql';
import { CURRENCY_OPTIONS, DIMENSION_UNITS, NotificationType, ServiceLevelType, WEIGHT_UNITS } from '@karrio/types';
import CodeMirror, { ReactCodeMirrorRef } from '@uiw/react-codemirror';
import { TabStateProvider, Tabs } from '../components/tabs';
import { useAPIMetadata } from '@karrio/hooks/api-metadata';
import { CheckBoxField, SelectField } from '../components';
import { failsafe, isEqual, isNone } from '@karrio/lib';
import { InputField } from '../components/input-field';
import { jsonLanguage } from '@codemirror/lang-json';
import { useNotifier } from '../components/notifier';
import { ModalFormProps, useModal } from './modal';
import { useLoader } from '../components/loader';
import React from 'react';

type RateSheetDataType = CreateRateSheetMutationInput & UpdateRateSheetMutationInput;
type RateSheetModalEditorProps = {
  header?: string;
  sheet?: RateSheetDataType;
  onSubmit: (sheet: RateSheetDataType) => Promise<any>;
};
const DEFAULT_STATE = {
  carrier_name: "generic",
  services: [
    {
      "currency": "USD",
      "service_code": "standard_service",
      "service_name": "Standard Service",
      "transit_days": 1,
      "weight_unit": "KG",
      "dimension_unit": "CM",
      "zones": [
        {
          "rate": 10.0
        }
      ]
    }
  ]
} as RateSheetDataType;

function reducer(state: RateSheetDataType, { name, value }: { name: string, value: string | boolean | Partial<RateSheetDataType> | object | string[] }): RateSheetDataType {
  switch (name) {
    case "full":
      return { ...(value as RateSheetDataType) };
    case "partial":
      return { ...state, ...(value as object) };
    default:
      return { ...state, [name]: value };
  }
}

export const RateSheetModalEditor: React.FC<ModalFormProps<RateSheetModalEditorProps>> = ({ trigger, ...args }) => {
  const modal = useModal();

  const FormComponent: React.FC<RateSheetModalEditorProps> = props => {
    const { sheet: defaultValue, header, onSubmit } = props;
    const editor = React.useRef<ReactCodeMirrorRef>(null);
    const loader = useLoader();
    const { close } = useModal();
    const notifier = useNotifier();
    const { loading } = useLoader();
    const { references: { service_levels } } = useAPIMetadata();
    const [key, setKey] = React.useState<string>(`sheet-${Date.now()}`);
    const [sheet, dispatch] = React.useReducer(reducer, defaultValue || DEFAULT_STATE, () => defaultValue || DEFAULT_STATE);

    const handleChange = (event: React.ChangeEvent<any>) => {
      const target = event.target;
      const name: string = target.name;
      let value = target.type === 'checkbox' ? target.checked : target.value;

      if (target.multiple === true) {
        value = Array.from(target.selectedOptions).map((o: any) => o.value)
      }

      dispatch({ name, value });
    };
    const computeDefaultCurrency = (defaultValue: ServiceLevelType[]): CurrencyCodeEnum => {
      const svc = (defaultValue || []).find(svc => !isNone(svc.currency))
      return (svc?.currency || CurrencyCodeEnum.USD) as CurrencyCodeEnum
    };
    const computeRates = (services: RateSheetDataType['services']) => {
      const max = Math.max(...(services || []).map(svc => svc.zones.length));
      return [{ max, services: services || [] }];
    };
    const updateServices = (key: string) => (e: React.ChangeEvent<any>) => {
      const newValue = (sheet.services || []).map(service => ({ ...service, [key]: e.target.value }));
      editor.current!.view?.dispatch({
        changes: { from: 0, to: editor.current!.view!.state.doc.length, insert: JSON.stringify(newValue, null, 2) }
      });
      dispatch({ name: 'services', value: newValue });
    };
    const updateSercice = (idx: number) => (event: React.ChangeEvent<any>) => {
      const target = event.target;
      const name: string = target.name;
      let value = target.type === 'checkbox' ? target.checked : target.value;
      if (target.multiple === true) {
        value = Array.from(target.selectedOptions).map((o: any) => o.value)
      }

      const newValue = (sheet.services || []).map((service, key) => key === idx ? { ...service, [name]: value } : service);
      editor.current!.view?.dispatch({
        changes: { from: 0, to: editor.current!.view!.state.doc.length, insert: JSON.stringify(newValue, null, 2) }
      });
      dispatch({ name: 'services', value: newValue });
    };

    const handleSubmit = async (e: React.FormEvent) => {
      e.preventDefault();
      const { ...payload } = sheet;
      try {
        loader.setLoading(true);
        onSubmit && onSubmit(payload);
      } catch (message: any) {
        notifier.notify({ type: NotificationType.error, message });
      }
      loader.setLoading(false);
    };

    return (
      <form className="modal-card-body p-4" onSubmit={handleSubmit} key={key}>
        {(sheet !== undefined) && <>

          <div className="pb-2 pt-0 is-flex is-justify-content-space-between has-background-white">
            <div className="is-vcentered">
              <button className="button is-white is-small" aria-label="close" onClick={close}>
                <span className="icon is-large">
                  <i className="fas fa-lg fa-times"></i>
                </span>
              </button>
              <span className="title is-6 has-text-weight-semibold px-2 py-3">{header || `Edit rate sheet`}</span>
            </div>
            <div>
              <button
                type="submit"
                className="button is-small is-success"
                disabled={loading || isEqual(sheet, defaultValue || DEFAULT_STATE) || !sheet.name || !sheet.carrier_name}
              >
                Save
              </button>
            </div>
          </div>

          <hr className='my-2' style={{ height: '1px' }} />

          <div className="columns m-0">

            <div className="column px-0 pb-4">

              <SelectField
                name="carrier_name"
                label="carrier name"
                onChange={handleChange}
                value={sheet.carrier_name || "generic"}
                className="is-small is-fullwidth"
                required
                disabled={!!sheet.id}
              >
                {Object.keys(service_levels).map(unit => <option key={unit} value={unit}>{unit}</option>)}
              </SelectField>

              <InputField label="name"
                name="name"
                onChange={handleChange}
                value={sheet.name || ''}
                placeholder="Courier negotiated rates"
                className="is-small"
                required
              />

              <SelectField
                name="currency"
                label="currency"
                onChange={updateServices('currency')}
                value={(sheet?.services || [])[0]?.currency || computeDefaultCurrency(service_levels[sheet.carrier_name] || [])}
                className="is-small is-fullwidth"
              >
                {CURRENCY_OPTIONS.map(unit => <option key={unit} value={unit}>{unit}</option>)}
              </SelectField>

              <SelectField
                name="weight_unit"
                label="weight_unit"
                onChange={updateServices('weight_unit')}
                value={(sheet?.services || [])[0]?.weight_unit || 'KG'}
                className="is-small is-fullwidth"
              >
                {WEIGHT_UNITS.map(unit => <option key={unit} value={unit}>{unit}</option>)}
              </SelectField>

              <SelectField
                name="dimension_unit"
                label="dimension_unit"
                onChange={updateServices('dimension_unit')}
                value={(sheet?.services || [])[0]?.dimension_unit || 'CM'}
                className="is-small is-fullwidth"
              >
                {DIMENSION_UNITS.map(unit => <option key={unit} value={unit}>{unit}</option>)}
              </SelectField>

            </div>

            <div className="p-3"></div>

            <div className="column p-0 is-9">

              <TabStateProvider tabs={['RATE SHEET', 'SERVICES', 'JSON EDITOR', 'SAMPLE']} setSelectedToURL={false}>
                <Tabs tabClass="is-size-6 has-text-weight-bold" style={{ position: 'relative' }}>
                  <div className="card" style={{ borderRadius: 0, height: '80vh', overflow: 'auto' }}>
                    <div className="table-container">
                      <table className="table is-bordered is-striped is-narrow">

                        <tbody>
                          {computeRates(sheet.services || [])
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

                          {(sheet.services || [])
                            .map((service, idx) => (
                              <tr key={`service-${idx}-${new Date()}`}>
                                <td className="is-size-7 p-0">
                                  <InputField
                                    name="service_name" onChange={updateSercice(idx)} value={service.service_name || ''} className="is-small"
                                  />
                                </td>
                                <td className="is-size-7 p-0">
                                  <InputField
                                    name="service_code" onChange={updateSercice(idx)} value={service.service_code || ''} className="is-small"
                                  />
                                </td>
                                <td className="is-size-7 p-0 is-vcentered">
                                  <CheckBoxField
                                    name="domicile" onChange={updateSercice(idx)} defaultChecked={service?.domicile as boolean} fieldClass="has-text-centered"
                                  />
                                </td>
                                <td className="is-size-7 p-0 is-vcentered">
                                  <CheckBoxField
                                    name="international" onChange={updateSercice(idx)} defaultChecked={service?.international as boolean} fieldClass="has-text-centered"
                                  />
                                </td>
                                <td className="is-size-7 p-0">
                                  <InputField
                                    name="transit_days" onChange={updateSercice(idx)} value={service.transit_days || ''} type='number' step={1} min={0} className="is-small"
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
                      value={failsafe(() => JSON.stringify(sheet.services || [], null, 2))}
                      onChange={value => failsafe(() => dispatch({ name: 'services', value: JSON.parse(value) }))}
                    />
                  </div>

                  <div className="card" style={{ borderRadius: 0 }}>
                    <CodeMirror
                      height="76vh"
                      extensions={[jsonLanguage]}
                      value={failsafe(() => JSON.stringify(service_levels[sheet.carrier_name], null, 2))}
                      editable={false}
                    />
                  </div>
                </Tabs>
              </TabStateProvider>

            </div>

          </div>

        </>}

      </form>
    )
  };

  return React.cloneElement(trigger, {
    onClick: () => modal.open(
      <FormComponent {...args} />,
      { className: 'is-large-modal', addCloseButton: false }
    )
  });
};
