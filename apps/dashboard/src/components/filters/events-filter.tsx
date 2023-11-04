import Dropdown, { closeDropdown } from '@/components/generic/dropdown';
import React, { useReducer, useContext, useEffect } from 'react';
import CheckBoxField from '@/components/generic/checkbox-field';
import InputField from '@/components/generic/input-field';
import { useEvents } from '@/context/event';
import Spinner from '@/components/spinner';
import { EVENT_TYPES } from '@/lib/types';
import { isNone } from '@/lib/helper';


interface EventsFilterComponent {
  context: ReturnType<typeof useEvents>;
}


const EventsFilter: React.FC<EventsFilterComponent> = ({ context }) => {
  const [isReady, setIsReady] = React.useState(true);
  const { query, filter: variables, setFilter } = context;
  const [filters, dispatch] = useReducer((state: any, { name, checked, value }: { name: string, checked?: boolean, value?: string | boolean | object }) => {
    switch (name) {
      case 'clear':
        return {};
      case 'full':
        return { ...(value as typeof variables) };
      case 'hasType':
        if (checked) return { ...state, type: [] };
        return Object.keys(state).reduce((acc, key) => key === 'type' ? acc : { ...acc, [key]: state[key] }, {});
      case 'type':
        return checked
          ? { ...state, type: [...(new Set([...state.type, value]) as any)] }
          : { ...state, type: state.type.filter((item: string) => item !== value) };
      case 'hasEntityId':
        if (checked) return { ...state, [value as string]: "" };
        return Object.keys(state).reduce((acc, key) => key === value ? acc : { ...acc, [key]: state[key] }, {});
      case 'hasDate':
        if (checked) return { ...state, date_before: "", date_after: "" };
        return Object.keys(state).reduce((acc, key) => ["date_before", "date_after"].includes(key) ? acc : { ...acc, [key]: state[key] }, {});
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

          {/* Type */}
          <div className="panel-block columns is-multiline m-0 p-0">

            <CheckBoxField defaultChecked={!isNone(filters?.type)} onChange={handleChange} name="hasType" fieldClass="column mb-0 is-12 px-2 py-2">
              <span>Event Type</span>
            </CheckBoxField>

            {!isNone(filters?.type) && <div className="column is-12 px-2 has-background-light">
              {EVENT_TYPES.map((type: string, index) => (
                <CheckBoxField key={index}
                  defaultChecked={filters?.type?.includes(type)}
                  onChange={handleChange}
                  name="type"
                  value={type}
                  fieldClass="is-fullwidth mb-0 py-1">
                  <span>{type}</span>
                </CheckBoxField>
              ))}
            </div>}

          </div>

        </>}

      </article>

    </Dropdown>
  );
}

export default EventsFilter;
