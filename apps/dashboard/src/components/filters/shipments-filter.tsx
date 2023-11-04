import Dropdown, { closeDropdown } from '@/components/generic/dropdown';
import CheckBoxField from '@/components/generic/checkbox-field';
import { CARRIER_NAMES, SHIPMENT_STATUSES } from '@/lib/types';
import InputField from '@/components/generic/input-field';
import React, { useReducer, useEffect } from 'react';
import { useShipments } from '@/context/shipment';
import Spinner from '@/components/spinner';
import { isNone } from '@/lib/helper';


interface ShipmentsFilterComponent {
  context: ReturnType<typeof useShipments>;
}


const ShipmentsFilter: React.FC<ShipmentsFilterComponent> = ({ context }) => {
  const [isReady, setIsReady] = React.useState(true);
  const { query, filter: variables, setFilter } = context;
  const [filters, dispatch] = useReducer((state: any, { name, checked, value }: { name: string, checked?: boolean, value?: string | boolean | object }) => {
    switch (name) {
      case 'clear':
        return {};
      case 'full':
        return { ...(value as typeof variables) };

      case 'hasStatus':
        if (checked) return { ...state, status: [] };
        return Object.keys(state).reduce((acc, key) => key === 'status' ? acc : { ...acc, [key]: state[key] }, {});
      case 'status':
        return checked
          ? { ...state, status: [...(new Set([...state.status, value]) as any)] }
          : { ...state, status: state.status.filter((item: string) => item !== value) };

      case 'hasService':
        if (checked) return { ...state, service: [] };
        return Object.keys(state).reduce((acc, key) => key === 'service' ? acc : { ...acc, [key]: state[key] }, {});
      case 'service':
        // return checked
        //   ? { ...state, service: [...(new Set([...state.service, value]) as any)] }
        //   : { ...state, service: state.service.filter((item: string) => item !== value) };
        return { ...state, [name]: [value] };

      case 'hasCarrierName':
        if (checked) return { ...state, carrier_name: [] };
        return Object.keys(state).reduce((acc, key) => key === 'carrier_name' ? acc : { ...acc, [key]: state[key] }, {});
      case 'carrier_name':
        return checked
          ? { ...state, carrier_name: [...(new Set([...state.carrier_name, value]) as any)] }
          : { ...state, carrier_name: state.carrier_name.filter((item: string) => item !== value) };

      case 'hasDate':
        if (checked) return { ...state, created_before: "", created_after: "" };
        return Object.keys(state).reduce((acc, key) => ["created_before", "created_after"].includes(key) ? acc : { ...acc, [key]: state[key] }, {});

      case 'hasAddress':
      case 'hasReference':
        if (checked) return { ...state, [value as string]: "" };
        return Object.keys(state).reduce((acc, key) => key === value ? acc : { ...acc, [key]: state[key] }, {});

      default:
        return { ...state, [name]: value };
    }
  }, variables, () => variables);

  const handleChange = (event: React.ChangeEvent<any> & CustomEvent<{ name: any, value: object }>) => {
    const target = event.target;
    const name = target.name;
    const value = target.value;
    const checked = target.type === 'checkbox' ? target.checked : undefined;

    dispatch({ name, value, checked });
  };
  const handleClear = (event: React.MouseEvent<HTMLButtonElement, MouseEvent>) => {
    event.preventDefault();
    setIsReady(false);
    dispatch({ name: 'clear' });
    window.setTimeout(() => {
      setIsReady(true);
    }, 200);
  };
  const handleApply = async (event: React.MouseEvent<HTMLButtonElement, MouseEvent>) => {
    event.preventDefault();
    setFilter({ ...filters, offset: 0 });
    closeDropdown(event.target);
  };

  useEffect(() => { dispatch({ name: 'full', value: variables }) }, [variables]);

  return (
    <Dropdown>

      {/* Dropdown trigger  */}
      <button className="button is-default is-small">
        <span className="icon is-small">
          <i className="fas fa-filter"></i>
        </span>
        <span className="is-size-6 has-text-weight-semibold">Filter</span>
      </button>

      {/* Dropdown content  */}
      <article className="menu-inner panel is-white p-0 has-background-white" style={{ width: '300px', maxHeight: '80vh', overflowY: 'auto', overflowX: 'hidden' }}>
        <div className="py-5"></div>
        <p className="panel-heading is-flex is-justify-content-space-between p-2 has-background-light"
          style={{ position: "absolute", top: 0, left: 0, right: 0, zIndex: 2 }}>
          <button className="button is-small is-default" onClick={handleClear}>Clear</button>
          <span className="is-size-6 has-text-weight-semibold p-1">Filters</span>
          <button
            className={"button is-small is-info" + (query.isFetching ? " is-loading" : "")}
            disabled={query.isFetching}
            onClick={handleApply}>Done</button>
        </p>

        {!isReady && <Spinner className="my-0 p-4 has-text-centered" />}

        {isReady && <>

          {/* Address */}
          <div className="panel-block columns is-multiline m-0 p-0">

            <CheckBoxField defaultChecked={!isNone(filters?.address)} onChange={handleChange} name="hasAddress" value="address" fieldClass="column mb-0 is-12 px-2 py-2">
              <span>Address</span>
            </CheckBoxField>

            {!isNone(filters?.address) && <div className="column is-12 px-2 has-background-light">
              <InputField
                defaultValue={filters?.address}
                onChange={handleChange}
                name="address"
                fieldClass="mb-0 py-1"
                className="is-fullwidth is-small"
                placeholder="e.g: 100 Main St, New York, NY"
              />
            </div>}

          </div>

          {/* Date */}
          <div className="panel-block columns is-multiline m-0 p-0">

            <CheckBoxField defaultChecked={!isNone(filters?.created_before) || !isNone(filters?.created_after)} onChange={handleChange} name="hasDate" fieldClass="column mb-0 is-12 px-2 py-2">
              <span>Date</span>
            </CheckBoxField>

            {(!isNone(filters?.created_before) || !isNone(filters?.created_after)) && <div className="column is-12 px-2 has-background-light">
              <InputField
                defaultValue={filters?.created_after}
                onChange={handleChange}
                type="datetime-local"
                name="created_after"
                fieldClass="has-addons mb-0 py-1"
                controlClass="is-expanded"
                className="is-small"
                addonLeft={
                  <p className="control">
                    <a className="button is-small is-static">after</a>
                  </p>
                }
              />
              <InputField
                defaultValue={filters?.created_before}
                onChange={handleChange}
                type="datetime-local"
                name="created_before"
                fieldClass="has-addons mb-0 py-1"
                controlClass="is-expanded"
                className="is-fullwidth is-small"
                addonLeft={
                  <p className="control">
                    <a className="button is-small is-static">before</a>
                  </p>
                }
              />
            </div>}

          </div>

          {/* Reference */}
          <div className="panel-block columns is-multiline m-0 p-0">

            <CheckBoxField defaultChecked={!isNone(filters?.reference)} onChange={handleChange} name="hasReference" value="reference" fieldClass="column mb-0 is-12 px-2 py-2">
              <span>Reference</span>
            </CheckBoxField>

            {!isNone(filters?.reference) && <div className="column is-12 px-2 has-background-light">
              <InputField
                defaultValue={filters?.reference}
                onChange={handleChange}
                name="reference"
                fieldClass="mb-0 py-1"
                className="is-fullwidth is-small"
                placeholder="e.g: Order #1111"
              />
            </div>}

          </div>

          {/* Service */}
          <div className="panel-block columns is-multiline m-0 p-0">

            <CheckBoxField defaultChecked={!isNone(filters?.service)} onChange={handleChange} name="hasService" value="service" fieldClass="column mb-0 is-12 px-2 py-2">
              <span>Service</span>
            </CheckBoxField>

            {!isNone(filters?.service) && <div className="column is-12 px-2 has-background-light">
              <InputField
                defaultValue={filters?.service}
                onChange={handleChange}
                name="service"
                fieldClass="mb-0 py-1"
                className="is-fullwidth is-small"
                placeholder="e.g: fedex_first_overnight"
              />
            </div>}

          </div>

          {/* Carrier Name */}
          <div className="panel-block columns is-multiline m-0 p-0">

            <CheckBoxField defaultChecked={!isNone(filters?.carrier_name)} onChange={handleChange} name="hasCarrierName" fieldClass="column mb-0 is-12 px-2 py-2">
              <span>Carrier</span>
            </CheckBoxField>

            {!isNone(filters?.carrier_name) && <div className="column is-12 px-2 has-background-light">
              {CARRIER_NAMES.map((carrier_name: string, index) => (
                <CheckBoxField key={index}
                  defaultChecked={filters?.carrier_name?.includes(carrier_name)}
                  onChange={handleChange}
                  name="carrier_name"
                  value={carrier_name}
                  fieldClass="is-fullwidth mb-0 py-1">
                  <span>{carrier_name}</span>
                </CheckBoxField>
              ))}
            </div>}

          </div>

          {/* Status */}
          <div className="panel-block columns is-multiline m-0 p-0">

            <CheckBoxField defaultChecked={!isNone(filters?.status)} onChange={handleChange} name="hasStatus" fieldClass="column mb-0 is-12 px-2 py-2">
              <span>Status</span>
            </CheckBoxField>

            {!isNone(filters?.status) && <div className="column is-12 px-2 has-background-light">
              {SHIPMENT_STATUSES.map((status: string, index) => (
                <CheckBoxField key={index}
                  defaultChecked={filters?.status?.includes(status)}
                  onChange={handleChange}
                  name="status"
                  value={status}
                  fieldClass="is-fullwidth mb-0 py-1">
                  <span>{status}</span>
                </CheckBoxField>
              ))}
            </div>}

          </div>

        </>}

      </article>

    </Dropdown>
  );
}

export default ShipmentsFilter;
