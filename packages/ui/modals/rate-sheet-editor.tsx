import {
  CreateRateSheetMutationInput,
  CurrencyCodeEnum,
  UpdateRateSheetMutationInput,
} from "@karrio/types/graphql";
import {
  CURRENCY_OPTIONS,
  DIMENSION_UNITS,
  NotificationType,
  ServiceLevelType,
  WEIGHT_UNITS,
} from "@karrio/types";
import CodeMirror, { ReactCodeMirrorRef } from "@uiw/react-codemirror";
import { TabStateProvider, Tabs } from "../components/tabs";
import { useAPIMetadata } from "@karrio/hooks/api-metadata";
import { CheckBoxField, SelectField } from "../components";
import { failsafe, isEqual, isNone } from "@karrio/lib";
import { InputField } from "../components/input-field";
import { jsonLanguage } from "@codemirror/lang-json";
import { useNotifier } from "../components/notifier";
import { ModalFormProps, useModal } from "./modal";
import { useLoader } from "../components/loader";
import React from "react";

type RateSheetDataType = CreateRateSheetMutationInput &
  UpdateRateSheetMutationInput;
type RateSheetModalEditorProps = {
  header?: string;
  sheet?: RateSheetDataType;
  onSubmit: (sheet: RateSheetDataType) => Promise<any>;
};
const DEFAULT_STATE = {
  carrier_name: "generic",
  services: [
    {
      currency: "USD",
      service_code: "standard_service",
      service_name: "Standard Service",
      transit_days: 1,
      weight_unit: "KG",
      dimension_unit: "CM",
      zones: [
        {
          rate: 10.0,
        },
      ],
    },
  ],
} as RateSheetDataType;

function reducer(
  state: RateSheetDataType,
  {
    name,
    value,
  }: {
    name: string;
    value: string | boolean | Partial<RateSheetDataType> | object | string[];
  },
): RateSheetDataType {
  switch (name) {
    case "full":
      return { ...(value as RateSheetDataType) };
    case "partial":
      return { ...state, ...(value as object) };
    default:
      return { ...state, [name]: value };
  }
}

export const RateSheetModalEditor = ({
  trigger,
  ...args
}: ModalFormProps<RateSheetModalEditorProps>): JSX.Element => {
  const modal = useModal();

  const FormComponent = (props: RateSheetModalEditorProps): JSX.Element => {
    const { sheet: defaultValue, header, onSubmit } = props;
    const loader = useLoader();
    const { close } = useModal();
    const notifier = useNotifier();
    const { loading } = useLoader();
    const editor = React.useRef<ReactCodeMirrorRef>(null);
    const [editingServiceIndex, setEditingServiceIndex] = React.useState<number | null>(null);
    const {
      references: { service_levels },
    } = useAPIMetadata();
    const [key, setKey] = React.useState<string>(`sheet-${Date.now()}`);
    const [sheet, dispatch] = React.useReducer(
      reducer,
      defaultValue || DEFAULT_STATE,
      () => defaultValue || DEFAULT_STATE,
    );

    const handleChange = (event: React.ChangeEvent<any>) => {
      const target = event.target;
      const name: string = target.name;
      let value = target.type === "checkbox" ? target.checked : target.value;

      if (target.multiple === true) {
        value = Array.from(target.selectedOptions).map((o: any) => o.value);
      }

      dispatch({ name, value });
    };
    const computeDefaultCurrency = (
      defaultValue: ServiceLevelType[],
    ): CurrencyCodeEnum => {
      const svc = (defaultValue || []).find((svc) => !isNone(svc.currency));
      return (svc?.currency || CurrencyCodeEnum.USD) as CurrencyCodeEnum;
    };
    const computeRates = (services: RateSheetDataType["services"]) => {
      const max = Math.max(...(services || []).map((svc) => svc.zones.length));
      return [{ max, services: services || [] }];
    };
    const updateServices = (key: string) => (e: React.ChangeEvent<any>) => {
      const newValue = (sheet.services || []).map((service) => ({
        ...service,
        [key]: e.target.value,
      }));
      editor.current!.view?.dispatch({
        changes: {
          from: 0,
          to: editor.current!.view!.state.doc.length,
          insert: JSON.stringify(newValue, null, 2),
        },
      });
      dispatch({ name: "services", value: newValue });
    };
    const updateSercice = (idx: number) => (event: React.ChangeEvent<any>) => {
      const target = event.target;
      const name: string = target.name;
      let value = target.type === "checkbox" ? target.checked : target.value;
      if (target.multiple === true) {
        value = Array.from(target.selectedOptions).map((o: any) => o.value);
      }

      const newValue = (sheet.services || []).map((service, key) =>
        key === idx ? { ...service, [name]: value } : service,
      );
      editor.current!.view?.dispatch({
        changes: {
          from: 0,
          to: editor.current!.view!.state.doc.length,
          insert: JSON.stringify(newValue, null, 2),
        },
      });
      dispatch({ name: "services", value: newValue });
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

    const handleServiceRowClick = (idx: number) => {
      setEditingServiceIndex(idx);
    };
    
    const closeServiceEdit = () => {
      setEditingServiceIndex(null);
    };

    return (
      <form className="modal-card-body p-4" onSubmit={handleSubmit} key={key}>
        {sheet !== undefined && (
          <>
            <div className="pb-2 pt-0 is-flex is-justify-content-space-between has-background-white">
              <div className="is-vcentered">
                <button
                  className="button is-white is-small"
                  aria-label="close"
                  onClick={close}
                >
                  <span className="icon is-large">
                    <i className="fas fa-lg fa-times"></i>
                  </span>
                </button>
                <span className="title is-6 has-text-weight-semibold px-2 py-3">
                  {header || `Edit rate sheet`}
                </span>
              </div>
              <div>
                <button
                  type="submit"
                  className="button is-small is-success"
                  disabled={
                    loading ||
                    isEqual(sheet, defaultValue || DEFAULT_STATE) ||
                    !sheet.name ||
                    !sheet.carrier_name
                  }
                >
                  Save
                </button>
              </div>
            </div>

            <hr className="my-2" style={{ height: "1px" }} />

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
                  {Object.keys(service_levels).map((unit) => (
                    <option key={unit} value={unit}>
                      {unit}
                    </option>
                  ))}
                </SelectField>

                <InputField
                  label="name"
                  name="name"
                  onChange={handleChange}
                  value={sheet.name || ""}
                  placeholder="Courier negotiated rates"
                  className="is-small"
                  required
                />

                <SelectField
                  name="currency"
                  label="currency"
                  onChange={updateServices("currency")}
                  value={
                    (sheet?.services || [])[0]?.currency ||
                    computeDefaultCurrency(
                      service_levels[sheet.carrier_name] || [],
                    )
                  }
                  className="is-small is-fullwidth"
                >
                  {CURRENCY_OPTIONS.map((unit) => (
                    <option key={unit} value={unit}>
                      {unit}
                    </option>
                  ))}
                </SelectField>

                <SelectField
                  name="weight_unit"
                  label="weight_unit"
                  onChange={updateServices("weight_unit")}
                  value={(sheet?.services || [])[0]?.weight_unit || "KG"}
                  className="is-small is-fullwidth"
                >
                  {WEIGHT_UNITS.map((unit) => (
                    <option key={unit} value={unit}>
                      {unit}
                    </option>
                  ))}
                </SelectField>

                <SelectField
                  name="dimension_unit"
                  label="dimension_unit"
                  onChange={updateServices("dimension_unit")}
                  value={(sheet?.services || [])[0]?.dimension_unit || "CM"}
                  className="is-small is-fullwidth"
                >
                  {DIMENSION_UNITS.map((unit) => (
                    <option key={unit} value={unit}>
                      {unit}
                    </option>
                  ))}
                </SelectField>
              </div>

              <div className="p-3"></div>

              <div className="column p-0 is-9">
                <TabStateProvider
                  tabs={["RATE SHEET", "SERVICES", "JSON EDITOR", "SAMPLE"]}
                  setSelectedToURL={false}
                >
                  <Tabs
                    tabClass="is-size-6 has-text-weight-bold"
                    style={{ position: "relative" }}
                  >
                    <div
                      className="card"
                      style={{
                        borderRadius: 0,
                        height: "80vh",
                        overflow: "auto",
                      }}
                    >
                      <div className="table-container">
                        <table className="table is-bordered is-striped is-narrow">
                          <tbody>
                            {computeRates(sheet.services || []).map(
                              ({ max, services }) => (
                                <React.Fragment key={`svc-${new Date()}`}>
                                  <tr
                                    style={{
                                      minWidth: "100px",
                                      position: "sticky",
                                      top: 0,
                                      left: 0,
                                      zIndex: 1,
                                    }}
                                    className="is-selected"
                                  >
                                    <td
                                      className="is-size-7 text-ellipsis is-info"
                                      style={{
                                        minWidth: "80px",
                                        position: "sticky",
                                        top: 0,
                                        left: 0,
                                        zIndex: 1,
                                      }}
                                    >
                                      zones
                                    </td>
                                    {services.map((service) => (
                                      <td
                                        key={service.service_code}
                                        className="is-size-7 text-ellipsis"
                                      >
                                        {service.service_code}
                                      </td>
                                    ))}
                                  </tr>

                                  {(services || []).length > 0 &&
                                    Array.from(Array(max).keys()).map(
                                      (__, idx) => (
                                        <tr key={`${idx}-${new Date()}`}>
                                          <td
                                            className="is-size-7 is-info"
                                            style={{
                                              minWidth: "80px",
                                              position: "sticky",
                                              top: 0,
                                              left: 0,
                                            }}
                                          >
                                            zone {idx}
                                          </td>
                                          {services.map((service, key) => (
                                            <td
                                              key={`${key}-${new Date()}`}
                                              className="is-size-7"
                                              style={{
                                                width: "100px",
                                                minWidth: "100px",
                                              }}
                                            >
                                              {service.zones[idx]?.rate || ""}
                                            </td>
                                          ))}
                                        </tr>
                                      ),
                                    )}
                                </React.Fragment>
                              ),
                            )}
                          </tbody>
                        </table>
                      </div>
                    </div>

                    <div
                      className="card"
                      style={{
                        borderRadius: 0,
                        height: "80vh",
                        overflow: "auto",
                      }}
                    >
                      <div className="table-container">
                        <table className="table is-bordered is-striped is-narrow is-hoverable">
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

                            {(sheet.services || []).map((service, idx) => (
                              <tr 
                                key={`service-${idx}-${new Date()}`}
                                onClick={() => handleServiceRowClick(idx)}
                                style={{ cursor: 'pointer' }}
                                className={idx === editingServiceIndex ? "is-selected" : ""}
                              >
                                <td className="is-size-7 p-0">
                                  <div className="input is-small">
                                    {service.service_name || ""}
                                  </div>
                                </td>
                                <td className="is-size-7 p-0">
                                  <div className="input is-small">
                                    {service.service_code || ""}
                                  </div>
                                </td>
                                <td className="is-size-7 p-0 is-vcentered has-text-centered">
                                  {service?.domicile ? "✓" : ""}
                                </td>
                                <td className="is-size-7 p-0 is-vcentered has-text-centered">
                                  {service?.international ? "✓" : ""}
                                </td>
                                <td className="is-size-7 p-0">
                                  <div className="input is-small">
                                    {service.transit_days || ""}
                                  </div>
                                </td>
                                <td className="is-size-7 p-0">
                                  <div className="input is-small">
                                    {service.transit_time || ""}
                                  </div>
                                </td>
                                <td className="is-size-7 p-0">
                                  <div className="input is-small">
                                    {service.max_weight || ""}
                                  </div>
                                </td>
                                <td className="is-size-7 p-0">
                                  <div className="input is-small">
                                    {service.max_length || ""}
                                  </div>
                                </td>
                                <td className="is-size-7 p-0">
                                  <div className="input is-small">
                                    {service.max_width || ""}
                                  </div>
                                </td>
                                <td className="is-size-7 p-0">
                                  <div className="input is-small">
                                    {service.max_height || ""}
                                  </div>
                                </td>
                              </tr>
                            ))}
                            {(sheet.services || []).length > 0 && (
                              <tr>
                                <td colSpan={10} className="has-text-centered">
                                  <button
                                    type="button"
                                    className="button is-small is-primary is-light"
                                    onClick={() => {
                                      const newServices = [...(sheet.services || [])];
                                      const lastService = newServices[newServices.length - 1] || (DEFAULT_STATE.services?.[0] || {
                                        currency: "USD",
                                        service_code: "standard_service",
                                        service_name: "Standard Service",
                                        transit_days: 1,
                                        weight_unit: "KG",
                                        dimension_unit: "CM",
                                        zones: [{ rate: 10.0 }],
                                      });
                                      newServices.push({
                                        ...lastService,
                                        service_name: `Service ${newServices.length + 1}`,
                                        service_code: `service_${newServices.length + 1}`,
                                        zones: lastService.zones.map(z => ({ ...z })),
                                      });
                                      dispatch({ name: "services", value: newServices });
                                      editor.current!.view?.dispatch({
                                        changes: {
                                          from: 0,
                                          to: editor.current!.view!.state.doc.length,
                                          insert: JSON.stringify(newServices, null, 2),
                                        },
                                      });
                                    }}
                                  >
                                    Add Service
                                  </button>
                                </td>
                              </tr>
                            )}
                          </tbody>
                        </table>
                      </div>
                      
                      {/* Service edit modal */}
                      {editingServiceIndex !== null && (
                        <div className="modal is-active">
                          <div className="modal-background" onClick={closeServiceEdit}></div>
                          <div className="modal-card" style={{ maxWidth: "800px", width: "100%" }}>
                            <header className="modal-card-head">
                              <p className="modal-card-title">Edit Service {sheet.services?.[editingServiceIndex]?.service_name}</p>
                              <button 
                                className="delete" 
                                aria-label="close" 
                                onClick={closeServiceEdit}
                              ></button>
                            </header>
                            <section className="modal-card-body">
                              <div className="table-container">
                                <table className="table is-bordered is-narrow">
                                  <tbody>
                                    <tr>
                                      <td className="is-size-7" width="200px">Service name</td>
                                      <td className="p-0">
                                        <InputField
                                          name="service_name"
                                          onChange={updateSercice(editingServiceIndex)}
                                          value={sheet.services?.[editingServiceIndex]?.service_name || ""}
                                          className="is-small"
                                          placeholder="e.g. Standard Service"
                                        />
                                      </td>
                                    </tr>
                                    <tr>
                                      <td className="is-size-7">Service code</td>
                                      <td className="p-0">
                                        <InputField
                                          name="service_code"
                                          onChange={updateSercice(editingServiceIndex)}
                                          value={sheet.services?.[editingServiceIndex]?.service_code || ""}
                                          className="is-small"
                                          placeholder="e.g. standard_service"
                                        />
                                        <p className="help is-size-7">friendly-tag, e.g. standard-service</p>
                                      </td>
                                    </tr>
                                    <tr>
                                      <td className="is-size-7">Transit days</td>
                                      <td className="p-0">
                                        <InputField
                                          name="transit_days"
                                          onChange={updateSercice(editingServiceIndex)}
                                          value={sheet.services?.[editingServiceIndex]?.transit_days || ""}
                                          type="text"
                                          inputMode="numeric"
                                          className="is-small no-spinner"
                                        />
                                      </td>
                                    </tr>
                                    <tr>
                                      <td className="is-size-7">Transit time</td>
                                      <td className="p-0">
                                        <InputField
                                          name="transit_time"
                                          onChange={updateSercice(editingServiceIndex)}
                                          value={sheet.services?.[editingServiceIndex]?.transit_time || ""}
                                          type="text"
                                          inputMode="numeric"
                                          className="is-small no-spinner"
                                        />
                                      </td>
                                    </tr>
                                    <tr>
                                      <td className="is-size-7">Max weight</td>
                                      <td className="p-0">
                                        <InputField
                                          name="max_weight"
                                          onChange={updateSercice(editingServiceIndex)}
                                          value={sheet.services?.[editingServiceIndex]?.max_weight || ""}
                                          type="text"
                                          inputMode="numeric"
                                          className="is-small no-spinner"
                                        />
                                      </td>
                                    </tr>
                                    <tr>
                                      <td className="is-size-7">Max length</td>
                                      <td className="p-0">
                                        <InputField
                                          name="max_length"
                                          onChange={updateSercice(editingServiceIndex)}
                                          value={sheet.services?.[editingServiceIndex]?.max_length || ""}
                                          type="text"
                                          inputMode="numeric"
                                          className="is-small no-spinner"
                                        />
                                      </td>
                                    </tr>
                                    <tr>
                                      <td className="is-size-7">Max width</td>
                                      <td className="p-0">
                                        <InputField
                                          name="max_width"
                                          onChange={updateSercice(editingServiceIndex)}
                                          value={sheet.services?.[editingServiceIndex]?.max_width || ""}
                                          type="text"
                                          inputMode="numeric"
                                          className="is-small no-spinner"
                                        />
                                      </td>
                                    </tr>
                                    <tr>
                                      <td className="is-size-7">Max height</td>
                                      <td className="p-0">
                                        <InputField
                                          name="max_height"
                                          onChange={updateSercice(editingServiceIndex)}
                                          value={sheet.services?.[editingServiceIndex]?.max_height || ""}
                                          type="text"
                                          inputMode="numeric"
                                          className="is-small no-spinner"
                                        />
                                      </td>
                                    </tr>
                                    <tr>
                                      <td className="is-size-7">National</td>
                                      <td className="p-0 is-vcentered">
                                        <CheckBoxField
                                          name="domicile"
                                          onChange={updateSercice(editingServiceIndex)}
                                          defaultChecked={sheet.services?.[editingServiceIndex]?.domicile as boolean}
                                          fieldClass="has-text-centered"
                                        />
                                      </td>
                                    </tr>
                                    <tr>
                                      <td className="is-size-7">International</td>
                                      <td className="p-0 is-vcentered">
                                        <CheckBoxField
                                          name="international"
                                          onChange={updateSercice(editingServiceIndex)}
                                          defaultChecked={sheet.services?.[editingServiceIndex]?.international as boolean}
                                          fieldClass="has-text-centered"
                                        />
                                      </td>
                                    </tr>
                                  </tbody>
                                </table>
                              </div>
                            </section>
                            <footer className="modal-card-foot">
                              <button 
                                className="button is-success is-small" 
                                onClick={closeServiceEdit}
                              >
                                Save changes
                              </button>
                              <button 
                                className="button is-small" 
                                onClick={closeServiceEdit}
                              >
                                Cancel
                              </button>
                              {editingServiceIndex > 0 && (
                                <button
                                  className="button is-danger is-light is-small ml-auto"
                                  onClick={() => {
                                    const newServices = [...(sheet.services || [])];
                                    newServices.splice(editingServiceIndex, 1);
                                    dispatch({ name: "services", value: newServices });
                                    editor.current!.view?.dispatch({
                                      changes: {
                                        from: 0,
                                        to: editor.current!.view!.state.doc.length,
                                        insert: JSON.stringify(newServices, null, 2),
                                      },
                                    });
                                    closeServiceEdit();
                                  }}
                                >
                                  Remove Service
                                </button>
                              )}
                            </footer>
                          </div>
                        </div>
                      )}
                    </div>

                    <div
                      className="card"
                      style={{ borderRadius: 0, overflow: "auto" }}
                    >
                      <div className="p-4">
                        <h3 className="title is-6 mb-4">Improved Service Editor (Comparison)</h3>
                        <table className="table is-fullwidth">
                          <tbody>
                            {(sheet.services || []).map((service, idx) => (
                              <React.Fragment key={`improved-service-${idx}`}>
                                <tr>
                                  <td colSpan={2} className="has-text-weight-bold">
                                    Service {idx + 1}
                                  </td>
                                </tr>
                                <tr>
                                  <td className="is-size-7" width="30%">Service name</td>
                                  <td>
                                    <InputField
                                      name="service_name"
                                      onChange={updateSercice(idx)}
                                      value={service.service_name || ""}
                                      className="is-small"
                                      placeholder="e.g. Standard Service"
                                    />
                                  </td>
                                </tr>
                                <tr>
                                  <td className="is-size-7">Service code</td>
                                  <td>
                                    <InputField
                                      name="service_code"
                                      onChange={updateSercice(idx)}
                                      value={service.service_code || ""}
                                      className="is-small"
                                      placeholder="e.g. standard_service"
                                    />
                                    <p className="help is-size-7">friendly-tag, e.g. standard-service</p>
                                  </td>
                                </tr>
                                <tr>
                                  <td className="is-size-7">Transit days</td>
                                  <td>
                                    <InputField
                                      name="transit_days"
                                      onChange={updateSercice(idx)}
                                      value={service.transit_days || ""}
                                      type="text"
                                      inputMode="numeric"
                                      className="is-small no-spinner"
                                    />
                                  </td>
                                </tr>
                                <tr>
                                  <td className="is-size-7">Transit time</td>
                                  <td>
                                    <InputField
                                      name="transit_time"
                                      onChange={updateSercice(idx)}
                                      value={service.transit_time || ""}
                                      type="text"
                                      inputMode="numeric"
                                      className="is-small no-spinner"
                                    />
                                  </td>
                                </tr>
                                <tr>
                                  <td className="is-size-7">Max weight</td>
                                  <td>
                                    <InputField
                                      name="max_weight"
                                      onChange={updateSercice(idx)}
                                      value={service.max_weight || ""}
                                      type="text"
                                      inputMode="numeric"
                                      className="is-small no-spinner"
                                    />
                                  </td>
                                </tr>
                                <tr>
                                  <td className="is-size-7">Max length</td>
                                  <td>
                                    <InputField
                                      name="max_length"
                                      onChange={updateSercice(idx)}
                                      value={service.max_length || ""}
                                      type="text"
                                      inputMode="numeric"
                                      className="is-small no-spinner"
                                    />
                                  </td>
                                </tr>
                                <tr>
                                  <td className="is-size-7">Max width</td>
                                  <td>
                                    <InputField
                                      name="max_width"
                                      onChange={updateSercice(idx)}
                                      value={service.max_width || ""}
                                      type="text"
                                      inputMode="numeric"
                                      className="is-small no-spinner"
                                    />
                                  </td>
                                </tr>
                                <tr>
                                  <td className="is-size-7">Max height</td>
                                  <td>
                                    <InputField
                                      name="max_height"
                                      onChange={updateSercice(idx)}
                                      value={service.max_height || ""}
                                      type="text"
                                      inputMode="numeric"
                                      className="is-small no-spinner"
                                    />
                                  </td>
                                </tr>
                                <tr>
                                  <td className="is-size-7">Domestic/International</td>
                                  <td>
                                    <div className="field is-grouped">
                                      <div className="control mr-4">
                                        <label className="checkbox">
                                          <CheckBoxField
                                            name="domicile"
                                            onChange={updateSercice(idx)}
                                            defaultChecked={service?.domicile as boolean}
                                          />
                                          <span className="ml-2 is-size-7">National</span>
                                        </label>
                                      </div>
                                      <div className="control">
                                        <label className="checkbox">
                                          <CheckBoxField
                                            name="international"
                                            onChange={updateSercice(idx)}
                                            defaultChecked={service?.international as boolean}
                                          />
                                          <span className="ml-2 is-size-7">International</span>
                                        </label>
                                      </div>
                                    </div>
                                  </td>
                                </tr>
                                {idx > 0 && (
                                  <tr>
                                    <td></td>
                                    <td className="has-text-right">
                                      <button
                                        type="button"
                                        className="button is-small is-danger is-light"
                                        onClick={() => {
                                          const newServices = [...(sheet.services || [])];
                                          newServices.splice(idx, 1);
                                          dispatch({ name: "services", value: newServices });
                                          editor.current!.view?.dispatch({
                                            changes: {
                                              from: 0,
                                              to: editor.current!.view!.state.doc.length,
                                              insert: JSON.stringify(newServices, null, 2),
                                            },
                                          });
                                        }}
                                      >
                                        Remove Service
                                      </button>
                                    </td>
                                  </tr>
                                )}
                                <tr>
                                  <td colSpan={2} style={{ height: "30px" }}></td>
                                </tr>
                              </React.Fragment>
                            ))}
                            <tr>
                              <td colSpan={2} className="has-text-centered">
                                <button
                                  type="button"
                                  className="button is-small is-primary is-light"
                                  onClick={() => {
                                    const newServices = [...(sheet.services || [])];
                                    const lastService = newServices[newServices.length - 1] || (DEFAULT_STATE.services?.[0] || {
                                      currency: "USD",
                                      service_code: "standard_service",
                                      service_name: "Standard Service",
                                      transit_days: 1,
                                      weight_unit: "KG",
                                      dimension_unit: "CM",
                                      zones: [{ rate: 10.0 }],
                                    });
                                    newServices.push({
                                      ...lastService,
                                      service_name: `Service ${newServices.length + 1}`,
                                      service_code: `service_${newServices.length + 1}`,
                                      zones: lastService.zones.map(z => ({ ...z })),
                                    });
                                    dispatch({ name: "services", value: newServices });
                                    editor.current!.view?.dispatch({
                                      changes: {
                                        from: 0,
                                        to: editor.current!.view!.state.doc.length,
                                        insert: JSON.stringify(newServices, null, 2),
                                      },
                                    });
                                  }}
                                >
                                  Add Service
                                </button>
                              </td>
                            </tr>
                          </tbody>
                        </table>
                      </div>
                      
                      {/* Original CodeMirror editor */}
                      <CodeMirror
                        ref={editor}
                        height="76vh"
                        extensions={[jsonLanguage]}
                        value={failsafe(() =>
                          JSON.stringify(sheet.services || [], null, 2),
                        )}
                        onChange={(value) =>
                          failsafe(() =>
                            dispatch({
                              name: "services",
                              value: JSON.parse(value),
                            }),
                          )
                        }
                      />
                    </div>

                    <div className="card" style={{ borderRadius: 0 }}>
                      {/* @ts-ignore */}
                      <CodeMirror
                        height="76vh"
                        extensions={[jsonLanguage]}
                        value={failsafe(() =>
                          JSON.stringify(
                            service_levels[sheet.carrier_name],
                            null,
                            2,
                          ),
                        )}
                        editable={false}
                      />
                    </div>
                  </Tabs>
                </TabStateProvider>
              </div>
            </div>
          </>
        )}
      </form>
    );
  };

  return React.cloneElement(trigger, {
    onClick: () =>
      modal.open(<FormComponent {...args} />, {
        className: "is-large-modal",
        addCloseButton: false,
      }),
  });
};
