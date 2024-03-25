import { DEFAULT_PARCEL_CONTENT, DIMENSION_UNITS, ParcelType, PresetCollection, ShipmentType, WEIGHT_UNITS } from '@karrio/types';
import { isEqual, findPreset, formatDimension, formatRef, isNone, validationMessage, validityCheck } from '@karrio/lib';
import React, { useEffect, useReducer, useState } from 'react';
import { CheckBoxField } from '../components/checkbox-field';
import { useAPIMetadata } from '@karrio/hooks/api-metadata';
import { useParcelTemplates } from '@karrio/hooks/parcel';
import { SelectField } from '../components/select-field';
import { InputField } from '../components/input-field';
import { WeightUnitEnum } from '@karrio/types';

type stateValue = string | number | boolean | Partial<ParcelType>;

interface ParcelFormComponent {
  value?: ParcelType;
  shipment?: ShipmentType;
  prefixChilren?: React.ReactNode;
  onChange?: (value: ParcelType) => void;
  children?: React.ReactNode;
}

function reducer(state: any, { name, value }: { name: string, value: stateValue }) {
  switch (name) {
    case 'template':
    case 'parcel_type':
    case 'package_preset':
      const { width, height, length, dimension_unit, packaging_type, package_preset } = value as ParcelType;
      return {
        ...state,
        width: width || null,
        height: height || null,
        length: length || null,
        dimension_unit: dimension_unit || null,
        packaging_type: packaging_type || null,
        package_preset: package_preset || null
      };
    default:
      return { ...state, [name]: value }
  }
}

export const ParcelForm: React.FC<ParcelFormComponent> = ({ value, shipment, children, prefixChilren, onChange }) => {
  const { references: { packaging_types, package_presets } } = useAPIMetadata();
  const { query } = useParcelTemplates();
  const [key] = useState<string>(`parcel-${Date.now()}`);
  const [parcel, dispatch] = useReducer(reducer, value, () => value || DEFAULT_PARCEL_CONTENT);
  const [parcel_type, setParcelType] = useState<string>(isNone(value?.package_preset) ? 'custom' : 'preset');
  const [dimension, setDimension] = useState<string | undefined>(formatDimension(isNone(value?.package_preset) ? undefined : value));

  const isDimensionRequired = (parcel: ParcelType) => {
    return !(
      isNone(parcel.width) &&
      isNone(parcel.height) &&
      isNone(parcel.length)
    );
  };
  const shouldShowDimension = (parcel_type: string) => {
    if (parcel_type === 'custom') return false;
    if (parcel_type !== 'preset') return true;
    if ((parcel.package_preset || "") !== "") return true;
    return false
  };

  const handleChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const target = event.target;
    let name: string = target.name;
    let value: stateValue = target.type === 'checkbox' ? target.checked : target.value;

    if (name === 'parcel_type') {
      const template = (query.data?.parcel_templates.edges || [])
        .find(p => p.node.id === value)?.node?.parcel;
      const preset = { ...parcel, package_preset: undefined } as Partial<ParcelType>;

      setParcelType(value as string);
      setDimension(formatDimension(value === 'custom' ? undefined : template || preset));
      value = { ...(template || preset as any), id: parcel.id };
      name = isNone(template) ? name : 'template';
    }
    else if (name === 'package_preset') {
      const preset = findPreset(package_presets as PresetCollection, value as string) || parcel;
      setDimension(formatDimension(preset));
      value = preset;
    }

    dispatch({ name, value: target.type === 'number' ? parseFloat(value as string) : value });
  };

  useEffect(() => {
    if (onChange && !isEqual(value, parcel)) {
      const { validation, ...changes } = parcel;
      onChange(changes);
    }
  }, [parcel]);

  return (
    <div key={key}>

      {/* Primary parcel form content */}
      {prefixChilren}

      {/* Default parcel form content */}
      <div className="columns m-0">

        <CheckBoxField name="is_document" onChange={handleChange}
          defaultChecked={parcel.is_document}
          fieldClass="column mb-0 is-12 px-1 py-2">
          <span>Document Only</span>
        </CheckBoxField>

      </div>

      <SelectField name="parcel_type" onChange={handleChange} value={parcel_type}
        className="is-small is-fullwidth"
        required>
        <optgroup label="New">
          <option value='custom'>Custom Measurements</option>
          <option value='preset'>Carrier Parcel Presets</option>
        </optgroup>
        {(!isNone(shipment) && (query.data?.parcel_templates.edges || []).length > 0) &&
          <optgroup label="Load your custom parcel template">
            {(query.data?.parcel_templates.edges || []).map(({ node: template }) => <option key={template.id} value={template.id}>{template.label}</option>)}
          </optgroup>}
      </SelectField>

      {(parcel_type === 'preset') && <>

        <SelectField name="package_preset" onChange={handleChange} value={parcel.package_preset}
          wrapperClass="mt-3"
          className="is-small is-fullwidth is-capitalized"
          required>
          <option value="">Select a Carrier Provided Parcel</option>

          {Object
            .entries(package_presets || {})
            .map(([key, value]) => (
              <optgroup key={key} label={formatRef(key)}>
                {Object.keys(value as object).map((preset) => (
                  <option key={preset} value={preset}>{formatRef(preset)}</option>
                ))}
              </optgroup>
            ))
          }
        </SelectField>

      </>}

      {shouldShowDimension(parcel_type) && <div className="is-size-7 mt-1 mb-2 has-text-grey">{dimension || ""}</div>}

      <div style={{ display: `${parcel_type === 'custom' ? 'block' : 'none'}` }}>
        <h6 className="is-size-7 my-2 has-text-weight-semibold">Dimensions</h6>

        <div className="columns mb-0 px-2">

          <SelectField name="packaging_type" onChange={handleChange} value={parcel.packaging_type}
            className="is-small is-fullwidth"
            wrapperClass="column is-4 px-1 py-2"
            fieldClass="mb-0 p-0"
            required
          >
            {packaging_types && Object
              .entries(packaging_types)
              .map(([key, value]) => (
                <optgroup key={key} label={formatRef(key)}>
                  {Object.keys(value as object).map((type) => (
                    <option key={type} value={type}>{formatRef(type)}</option>
                  ))}
                </optgroup>
              ))
            }
          </SelectField>

          <span className="is-size-7 mt-4">L:</span>
          <InputField
            type="number" step="any" min="0"
            name="length"
            onChange={validityCheck(handleChange)}
            value={parcel.length}
            className="is-small"
            wrapperClass="px-1 py-2"
            fieldClass="column mb-0 p-0"
            required={isDimensionRequired(parcel)}
            onInvalid={validityCheck(validationMessage('Please enter a valid length'))}
          />

          <span className="is-size-7 mt-4">W:</span>
          <InputField
            type="number" step="any" min="0"
            name="width"
            onChange={validityCheck(handleChange)}
            value={parcel.width}
            className="is-small"
            wrapperClass="px-1 py-2"
            fieldClass="column mb-0 p-0"
            required={isDimensionRequired(parcel)}
            onInvalid={validityCheck(validationMessage('Please enter a valid width'))}
          />

          <span className="is-size-7 mt-4">H:</span>
          <InputField
            type="number" step="any" min="0"
            name="height"
            onChange={validityCheck(handleChange)}
            value={parcel.height}
            className="is-small"
            wrapperClass="px-1 py-2"
            fieldClass="column mb-0 p-0"
            required={isDimensionRequired(parcel)}
            onInvalid={validityCheck(validationMessage('Please enter a valid height'))}
          />

          <SelectField name="dimension_unit"
            onChange={handleChange}
            value={parcel.dimension_unit}
            className="is-small is-fullwidth"
            wrapperClass="column is-2 px-1 py-2"
            fieldClass="mb-0 p-0"
            required={isDimensionRequired(parcel)}>
            {DIMENSION_UNITS.map(unit => <option key={unit} value={unit}>{unit}</option>)}
          </SelectField>

        </div>

      </div>

      <h6 className="is-size-7 my-2 has-text-weight-semibold">Weight</h6>

      <div className="columns mb-4 px-2">

        <InputField
          type="number" step="any" min="0"
          name="weight"
          value={parcel.weight || ""}
          className="is-small"
          wrapperClass="column is-2 px-1 py-2"
          fieldClass="mb-0 p-0"
          onChange={validityCheck(handleChange)}
          onInvalid={validityCheck(validationMessage('Please enter a valid weight'))}
          required
        />

        <SelectField
          name="weight_unit"
          onChange={handleChange}
          value={parcel.weight_unit || WeightUnitEnum.KG}
          className="is-small is-fullwidth"
          wrapperClass="column is-2 px-1 py-2"
          fieldClass="mb-0 p-0"
          required>
          {WEIGHT_UNITS.map(unit => <option key={unit} value={unit}>{unit}</option>)}
        </SelectField>

      </div>

      {/* Extra parcel form content */}
      {children}

    </div>
  )
};
