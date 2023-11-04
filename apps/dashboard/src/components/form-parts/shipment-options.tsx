import MetadataEditor, { MetadataEditorContext } from '@/components/metadata-editor';
import { CURRENCY_OPTIONS, NotificationType, ShipmentType } from '@/lib/types';
import React, { FormEvent, useContext, useReducer, useState } from 'react';
import CheckBoxField from '@/components/generic/checkbox-field';
import ButtonField from '@/components/generic/button-field';
import SelectField from '@/components/generic/select-field';
import { cleanDict, deepEqual, isNone } from '@/lib/helper';
import InputField from '@/components/generic/input-field';
import { MetadataObjectTypeEnum } from 'karrio/graphql';
import { Notify } from '@/components/notifier';
import { Loading } from '@/components/loader';

interface ShipmentOptionsComponent {
  shipment: ShipmentType;
  onSubmit: (changes: Partial<ShipmentType>) => Promise<any>;
}

function reducer(state: any, { name, value }: { name: string, value: string | boolean }) {
  switch (name) {
    case 'addCOD':
      return cleanDict<any>({ ...state, cash_on_delivery: value === true ? "" : undefined });
    case 'addInsurance':
      return cleanDict<any>({ ...state, insurance: value === true ? "" : undefined });
    case 'addDeclaredValue':
      return cleanDict<any>({ ...state, declared_value: value === true ? "" : undefined });
    default:
      return cleanDict<any>({ ...state, [name]: value || undefined });
  };
}

const ShipmentOptions: React.FC<ShipmentOptionsComponent> = ({ shipment, onSubmit }) => {
  const { notify } = useContext(Notify);
  const { loading, setLoading } = useContext(Loading);
  const [options, dispatch] = useReducer(reducer, shipment?.options, () => shipment?.options);
  const [metadata, setMetadata] = useState<any>(shipment?.metadata);
  const [reference, setReference] = useState(shipment?.reference);

  const computeDisable = (shipment: ShipmentType, options: any, metadata: any, reference?: string | null) => {
    return (
      (deepEqual(shipment.options, options) || (options === ({} as any) && shipment.options === ({} as any)))
      && (deepEqual(shipment.metadata, metadata) || (metadata === ({} as any) && shipment.metadata === ({} as any)))
      && shipment.reference === reference
    )
  }
  const handleChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const target = event.target;
    const name: string = target.name;
    const value = target.type === 'checkbox' ? target.checked : target.value;

    dispatch({ name, value });
  };
  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    try {
      if (shipment.id !== undefined) {
        setLoading(true);
        await onSubmit({ options, metadata, reference });
        notify({ type: NotificationType.success, message: 'Shipment options successfully updated!' });
      } else {
        await onSubmit({ options, metadata, reference });
      }
    } catch (message: any) {
      notify({ type: NotificationType.error, message });
    }
    setLoading(false);
  };

  return (
    <form className="px-1 py-2" onSubmit={handleSubmit}>

      <div className="">

        <InputField
          label="Shipment reference"
          name="reference"
          defaultValue={reference as string}
          onChange={e => setReference(e.target.value || null)}
          placeholder="shipment reference"
          className="is-small"
          autoComplete="off" />

      </div>

      <hr className="column p-0 my-5" />

      <div className="columns is-multiline mb-0">

        <InputField defaultValue={options?.shipment_date} onChange={handleChange} label="shipment date" name="shipment_date" type="date" className="is-small" fieldClass="column mb-0 is-5 px-2 py-2" />

        <CheckBoxField defaultChecked={options?.signature_confirmation} onChange={handleChange} name="signature_confirmation" fieldClass="column mb-0 is-12 px-2 py-2">
          <span>Add signature confirmation</span>
        </CheckBoxField>

      </div>


      <div className="columns is-multiline mb-0 pt-2">

        <CheckBoxField defaultChecked={!isNone(options?.insurance)} onChange={handleChange} name="addInsurance" fieldClass="column mb-0 is-12 px-2 py-2">
          <span>Add insurance</span>
        </CheckBoxField>

        <div className="column is-multiline mb-0 ml-6 my-1 px-2 py-0 is-12" style={{ borderLeft: "solid 2px #ddd", display: `${isNone(options?.insurance) ? 'none' : 'block'}` }}>

          <InputField defaultValue={options?.insurance} onChange={handleChange} label="Coverage value" name="insurance" type="number" min={0} step="any" className="is-small" controlClass="has-icons-left has-icons-right" fieldClass="column mb-0 is-4 px-1 py-2" required={!isNone(options?.insurance)}>
            <span className="icon is-small is-left">
              <i className="fas fa-dollar-sign"></i>
            </span>
            <span className="icon is-small is-right">{options?.currency}</span>
          </InputField>

        </div>
      </div>

      <div className="columns is-multiline mb-0 px-1 my-2">

        <SelectField label="shipment currency" value={options?.currency} onChange={handleChange} name="currency" className="is-small is-fullwidth" fieldClass="column is-4 mb-0 px-1 py-2" required={!isNone(options?.insurance) || !isNone(options?.cash_on_delivery) || !isNone(options?.declared_value)}>
          <option value="">Select a currency</option>

          {CURRENCY_OPTIONS.map(unit => <option key={unit} value={unit}>{unit}</option>)}
        </SelectField>

      </div>

      <div className="columns is-multiline mb-0 pt-2">

        <CheckBoxField defaultChecked={!isNone(options?.cash_on_delivery)} onChange={handleChange} name="addCOD" fieldClass="column mb-0 is-12 px-2 py-2">
          <span>Collect On Delivery</span>
        </CheckBoxField>

        <div className="column is-multiline mb-0 ml-6 my-1 px-2 py-0 is-12" style={{ borderLeft: "solid 2px #ddd", display: `${isNone(options?.cash_on_delivery) ? 'none' : 'block'}` }}>

          <InputField defaultValue={options?.cash_on_delivery} onChange={handleChange} label="Amount to collect" name="cash_on_delivery" type="number" min={0} step="any" className="is-small" controlClass="has-icons-left has-icons-right" fieldClass="column mb-0 is-4 px-1 py-2" required={!isNone(options?.cash_on_delivery)}>
            <span className="icon is-small is-left">
              <i className="fas fa-dollar-sign"></i>
            </span>
            <span className="icon is-small is-right">{options?.currency}</span>
          </InputField>

        </div>

      </div>


      <div className="columns is-multiline mb-0 pt-2">

        <CheckBoxField defaultChecked={!isNone(options?.declared_value)} onChange={handleChange} name="addDeclaredValue" fieldClass="column mb-0 is-12 px-2 py-2">
          <span>Add Total Value</span>
        </CheckBoxField>

        <div className="column is-multiline mb-0 ml-6 my-1 px-2 py-0 is-12" style={{ borderLeft: "solid 2px #ddd", display: `${isNone(options?.declared_value) ? 'none' : 'block'}` }}>

          <InputField defaultValue={options?.declared_value} onChange={handleChange} label="Package value" name="declared_value" type="number" min={0} step="any" className="is-small" controlClass="has-icons-left has-icons-right" fieldClass="column mb-0 is-4 px-1 py-2" required={!isNone(options?.declared_value)}>
            <span className="icon is-small is-left">
              <i className="fas fa-dollar-sign"></i>
            </span>
            <span className="icon is-small is-right">{options?.currency}</span>
          </InputField>

        </div>
      </div>

      <hr className="column p-0 my-5" />

      <MetadataEditor
        object_type={MetadataObjectTypeEnum.shipment}
        metadata={metadata}
        onChange={setMetadata}
      >
        <MetadataEditorContext.Consumer>{({ isEditing, editMetadata }) => (<>

          <div className="is-flex is-justify-content-space-between">
            <h2 className="title is-6 my-3">Metadata</h2>

            <button
              type="button"
              className="button is-default is-small is-align-self-center"
              disabled={isEditing}
              onClick={() => editMetadata()}>
              <span className="icon is-small">
                <i className="fas fa-pen"></i>
              </span>
              <span>Edit metadata</span>
            </button>
          </div>

          <hr className="mt-1 my-1" style={{ height: '1px' }} />

        </>)}</MetadataEditorContext.Consumer>
      </MetadataEditor>

      <div className="p-3 my-5"></div>
      <ButtonField type="submit"
        className={`is-primary ${loading ? 'is-loading' : ''} m-0`}
        fieldClass="form-floating-footer p-3"
        controlClass="has-text-centered"
        disabled={computeDisable(shipment, options, metadata, reference)}>
        <span>Save</span>
      </ButtonField>

    </form>
  )
};

export default ShipmentOptions;
