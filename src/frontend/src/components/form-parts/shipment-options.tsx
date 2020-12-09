import { Payment, Shipment } from '@purplship/purplship';
import React, { ChangeEvent, FormEvent, useRef, useState } from 'react';
import ButtonField from '@/components/generic/button-field';
import InputField from '../generic/input-field';
import CheckBoxField from '../generic/checkbox-field';
import SelectField from '../generic/select-field';
import { NotificationType, state } from '@/library/api';

interface ShipmentOptionsComponent {
    shipment: Shipment;
    update: (payload: {}) => void;
}

const ShipmentOptions: React.FC<ShipmentOptionsComponent> = ({ shipment, update }) => {
    const [options, setOptions] = useState<any>(shipment?.options || {});
    const [addInsurance, setAddInsurance] = useState<boolean>(false);
    const [addCOD, setCOD] = useState<boolean>(false);
    const form = useRef<any>(null);
    const _ = (e: ChangeEvent<any> & CustomEvent<{ name: string, value: object }>) => {
        e.stopPropagation();
        let new_state: any = {};
        if (e.detail !== undefined) {
            const property: string = e.detail.name;
            new_state = { ...options, [property]: { ...options[property], ...e.detail.value } };
        } else {
            const property: string = e.target.name;
            new_state = { ...options, [property]: e.target.type === 'checkbox' ? e.target.checked : e.target.value };
        }

        if (!addCOD) delete new_state.cash_on_delivery;
        if (!addInsurance) delete new_state.insurance;
        setOptions(new_state);
    };
    form?.current?.addEventListener('change', _);
    const handleSubmit = async (e: FormEvent) => {
        e.preventDefault();
        try {
            let data = { options };
            if (shipment.id !== undefined) {
                const updated_options = await state.setOptions(shipment.id, options);
                data = { options: updated_options };
                state.setNotification({ type: NotificationType.success, message: 'Shipment Options successfully updated!' });
            }
            update(data);
        } catch (err) {
            state.setNotification({ type: NotificationType.error, message: err });
        }
    };

    return (
        <form className="px-1 py-2" onSubmit={handleSubmit} ref={form}>

            <div className="columns is-multiline mb-0">

                <InputField label="shipment date" defaultValue={options.shipment_date} name="shipment_date" type="date" className="is-small" fieldClass="column mb-0 is-5 px-2 py-2" />

                <CheckBoxField defaultChecked={options.signature_confirmation} name="signature_confirmation" fieldClass="column mb-0 is-12 px-2 py-2">
                    <span>Add signature confirmation</span>
                </CheckBoxField>

            </div>


            <div className="columns is-multiline mb-0 pt-2">

                <CheckBoxField defaultChecked={addInsurance} onChange={() => setAddInsurance(!addInsurance)} fieldClass="column mb-0 is-12 px-2 py-2">
                    <span>Add insurance</span>
                </CheckBoxField>

                <div className="column is-multiline mb-0 ml-6 my-1 px-2 py-0 is-12" style={{ borderLeft: "solid 2px #ddd", display: `${addInsurance ? 'block': 'none'}` }}>

                    <InputField defaultValue={options.insurance} label="Total package value" name="insurance" type="number" min={0} className="is-small" controlClass="has-icons-left has-icons-right" fieldClass="column mb-0 is-4 px-1 py-2" required={addInsurance}>
                        <span className="icon is-small is-left">
                            <i className="fas fa-dollar-sign"></i>
                        </span>
                        <span className="icon is-small is-right">{options.currency}</span>
                    </InputField>

                </div>
            </div>


            <div className="columns is-multiline mb-0 pt-2">

                <CheckBoxField defaultChecked={addCOD} onChange={() => setCOD(!addCOD)} fieldClass="column mb-0 is-12 px-2 py-2">
                    <span>Collect On Delivery</span>
                </CheckBoxField>

                <div className="column is-multiline mb-0 ml-6 my-1 px-2 py-0 is-12" style={{ borderLeft: "solid 2px #ddd", display: `${addCOD ? 'block': 'none'}` }}>

                    <InputField defaultValue={options.cash_on_delivery} label="Amount to collect" name="cash_on_delivery" type="number" min={0} className="is-small" controlClass="has-icons-left has-icons-right" fieldClass="column mb-0 is-4 px-1 py-2" required={addCOD}>
                        <span className="icon is-small is-left">
                            <i className="fas fa-dollar-sign"></i>
                        </span>
                        <span className="icon is-small is-right">{options.currency}</span>
                    </InputField>

                </div>

            </div>

            <div className="columns is-multiline mb-0">

                <SelectField label="shipment currency" value={options.currency} name="currency" className="is-small is-fullwidth" fieldClass="column is-3 mb-0 px-1 py-2" required={addInsurance || addCOD}>
                    <option value="">Select a currency</option>

                    {Object.keys(Payment.CurrencyEnum).map(unit => (
                        <option key={unit} value={unit}>{unit}</option>
                    ))}
                </SelectField>

            </div>


            <ButtonField type="submit" className="is-primary" fieldClass="has-text-centered mt-3" disabled={shipment.options == options}>
                <span>Save</span>
            </ButtonField>

        </form>
    )
};

export default ShipmentOptions;