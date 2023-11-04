import Dropdown, { closeDropdown } from '@/components/generic/dropdown';
import CheckBoxField from '@/components/generic/checkbox-field';
import { HTTP_METHODS, HTTP_STATUS_CODES } from '@/lib/types';
import InputField from '@/components/generic/input-field';
import React, { useReducer, useEffect } from 'react';
import Spinner from '@/components/spinner';
import { useLogs } from '@/context/log';
import { isNone } from '@/lib/helper';


interface LogsFilterComponent {
  context: ReturnType<typeof useLogs>;
}


const LogsFilter: React.FC<LogsFilterComponent> = ({ context }) => {
  const { query, filter: variables, setFilter } = context;
  const [filters, dispatch] = useReducer((state: any, { name, checked, value }: { name: string, checked?: boolean, value?: string | boolean | object }) => {
    switch (name) {
      case 'clear':
        return {};
      case 'full':
        return { ...(value as typeof variables) };
      case 'hasStatus':
        if (checked) return { ...state, status_code: [] };
        return Object.keys(state).reduce((acc, key) => key === 'status_code' ? acc : { ...acc, [key]: state[key] }, {});
      case 'status_code':
        return checked
          ? { ...state, status_code: [...(new Set([...state.status_code, parseInt(value as string)]) as any)] }
          : { ...state, status_code: state.status_code.filter((item: number) => item !== parseInt(value as string)) };
      case 'hasMethod':
        if (checked) return { ...state, method: [] };
        return Object.keys(state).reduce((acc, key) => key === 'method' ? acc : { ...acc, [key]: state[key] }, {});
      case 'method':
        return checked
          ? { ...state, method: [...(new Set([...state.method, value]) as any)] }
          : { ...state, method: state.method.filter((item: string) => item !== value) };
      case 'hasEntityId':
      case 'hasEndpoint':
        if (checked) return { ...state, [value as string]: "" };
        return Object.keys(state).reduce((acc, key) => key === value ? acc : { ...acc, [key]: state[key] }, {});
      case 'hasDate':
        if (checked) return { ...state, date_before: "", date_after: "" };
        return Object.keys(state).reduce((acc, key) => ["date_before", "date_after"].includes(key) ? acc : { ...acc, [key]: state[key] }, {});
      default:
        return { ...state, [name]: value };
    }
  }, variables, () => variables);
  const [isReady, setIsReady] = React.useState(true);

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
    }, 500);
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

          {/* Date */}
          <div className="panel-block columns is-multiline m-0 p-0">

            <CheckBoxField defaultChecked={!isNone(filters?.date_before) || !isNone(filters?.date_after)} onChange={handleChange} name="hasDate" fieldClass="column mb-0 is-12 px-2 py-2">
              <span>Date</span>
            </CheckBoxField>

            {(!isNone(filters?.date_before) || !isNone(filters?.date_after)) && <div className="column is-12 px-2 has-background-light">
              <InputField
                defaultValue={filters?.date_after}
                onChange={handleChange}
                type="datetime-local"
                name="date_after"
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
                defaultValue={filters?.date_before}
                onChange={handleChange}
                type="datetime-local"
                name="date_before"
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

          {/* API Endpoint */}
          <div className="panel-block columns is-multiline m-0 p-0">

            <CheckBoxField defaultChecked={!isNone(filters?.api_endpoint)} onChange={handleChange} name="hasEndpoint" value="api_endpoint" fieldClass="column mb-0 is-12 px-2 py-2">
              <span>API Endpoint</span>
            </CheckBoxField>

            {!isNone(filters?.api_endpoint) && <div className="column is-12 px-2 has-background-light">
              <InputField
                defaultValue={filters?.api_endpoint}
                onChange={handleChange}
                name="api_endpoint"
                fieldClass="mb-0 py-1"
                className="is-fullwidth is-small"
                placeholder="e.g: /v1/trackers"
              />
            </div>}

          </div>

          {/* Remote Address */}
          <div className="panel-block columns is-multiline m-0 p-0">

            <CheckBoxField defaultChecked={!isNone(filters?.remote_addr)} onChange={handleChange} name="hasEndpoint" value="remote_addr" fieldClass="column mb-0 is-12 px-2 py-2">
              <span>Remote Address</span>
            </CheckBoxField>

            {!isNone(filters?.remote_addr) && <div className="column is-12 px-2 has-background-light">
              <InputField
                defaultValue={filters?.remote_addr}
                onChange={handleChange}
                name="remote_addr"
                fieldClass="mb-0 py-1"
                className="is-fullwidth is-small"
                placeholder="e.g: 192.168.0.1"
              />
            </div>}

          </div>

          {/* Entity ID */}
          <div className="panel-block columns is-multiline m-0 p-0">

            <CheckBoxField defaultChecked={!isNone(filters?.entity_id)} onChange={handleChange} name="hasEntityId" value="entity_id" fieldClass="column mb-0 is-12 px-2 py-2">
              <span>Related Object ID</span>
            </CheckBoxField>

            {!isNone(filters?.entity_id) && <div className="column is-12 px-2 has-background-light">
              <InputField
                defaultValue={filters?.entity_id}
                onChange={handleChange}
                name="entity_id"
                fieldClass="mb-0 py-1"
                className="is-fullwidth is-small"
                placeholder="e.g: shp_123456"
              />
            </div>}

          </div>

          {/* Method */}
          <div className="panel-block columns is-multiline m-0 p-0">

            <CheckBoxField defaultChecked={!isNone(filters?.method)} onChange={handleChange} name="hasMethod" fieldClass="column mb-0 is-12 px-2 py-2">
              <span>Method</span>
            </CheckBoxField>

            {!isNone(filters?.method) && <div className="column is-12 px-2 has-background-light">
              {HTTP_METHODS.map((method: string, index) => (
                <CheckBoxField key={index}
                  defaultChecked={filters?.method?.includes(method)}
                  onChange={handleChange}
                  name="method"
                  value={method}
                  fieldClass="is-fullwidth mb-0 py-1">
                  <span>{method}</span>
                </CheckBoxField>
              ))}
            </div>}

          </div>

          {/* Status Code */}
          <div className="panel-block columns is-multiline m-0 p-0">

            <CheckBoxField defaultChecked={!isNone(filters?.status_code)} onChange={handleChange} name="hasStatus" fieldClass="column mb-0 is-12 px-2 py-2">
              <span>Status Code</span>
            </CheckBoxField>

            {!isNone(filters?.status_code) && <div className="column is-12 px-2 has-background-light">
              {HTTP_STATUS_CODES.map((status: number, index) => (
                <CheckBoxField key={index}
                  defaultChecked={filters?.status_code?.includes(status)}
                  onChange={handleChange}
                  name="status_code"
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

export default LogsFilter;
