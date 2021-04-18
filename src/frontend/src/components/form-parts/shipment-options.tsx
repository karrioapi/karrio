import { PaymentCurrencyEnum, Shipment } from '@/api';
import React, { FormEvent, useContext, useReducer } from 'react';
import ButtonField from '@/components/generic/button-field';
import InputField from '@/components/generic/input-field';
import CheckBoxField from '@/components/generic/checkbox-field';
import SelectField from '@/components/generic/select-field';
import { cleanDict, deepEqual, isNone } from '@/library/helper';
import { NotificationType } from '@/library/types';
import ShipmentMutation from '../data/shipment-mutation';
import { Notify } from '../notifier';

interface ShipmentOptionsComponent {
    shipment: Shipment;
    update: (data: { changes?: Partial<Shipment>, refresh?: boolean }) => void;
}

function reducer(state: any, { name, value }: { name: string, value: string | boolean }) {
    switch (name) {
        case 'addCOD':
            return cleanDict<any>({ ...state, cash_on_delivery: value === true ? "" : undefined });
        case 'addInsurance':
            return cleanDict<any>({ ...state, insurance: value === true ? "" : undefined });
        default:
            return cleanDict<any>({ ...state, [name]: value || undefined });
    };
}

const ShipmentOptions: React.FC<ShipmentOptionsComponent> = ShipmentMutation<ShipmentOptionsComponent>(({ shipment, update, setOptions }) => {
    const { notify } = useContext(Notify);
    const [options, dispatch] = useReducer(reducer, shipment?.options, () => shipment?.options);

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
                await setOptions(shipment.id, options);
                notify({ type: NotificationType.success, message: 'Shipment Options successfully updated!' });
                update({refresh: true});
            } else {
                update({ changes: {options} });
            }
        } catch (err) {
            notify({ type: NotificationType.error, message: err });
        }
    };

    return (
        <form className="px-1 py-2" onSubmit={handleSubmit}>

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

                    <InputField defaultValue={options?.insurance} onChange={handleChange} label="Total package value" name="insurance" type="number" min={0} step="any" className="is-small" controlClass="has-icons-left has-icons-right" fieldClass="column mb-0 is-4 px-1 py-2" required={!isNone(options?.insurance)}>
                        <span className="icon is-small is-left">
                            <i className="fas fa-dollar-sign"></i>
                        </span>
                        <span className="icon is-small is-right">{options?.currency}</span>
                    </InputField>

                </div>
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

            <div className="columns is-multiline mb-0">

                <SelectField label="shipment currency" value={options?.currency} onChange={handleChange} name="currency" className="is-small is-fullwidth" fieldClass="column is-3 mb-0 px-1 py-2" required={!isNone(options?.insurance) || !isNone(options?.cash_on_delivery)}>
                    <option value="">Select a currency</option>

                    {Object.keys(PaymentCurrencyEnum).map(unit => (
                        <option key={unit} value={unit}>{unit}</option>
                    ))}
                </SelectField>

            </div>


            <ButtonField type="submit" className="is-primary" fieldClass="has-text-centered mt-3" disabled={deepEqual(shipment.options, options) || (options === {} && shipment.options === {})}>
                <span>{shipment.id === undefined ? 'Continue' : 'Save'}</span>
            </ButtonField>

        </form>
    )
});

export default ShipmentOptions;