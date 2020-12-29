import { Address, Shipment } from '@purplship/purplship';
import React, { FormEvent, useContext, useEffect, useReducer, useRef, useState } from 'react';
import { deepEqual, isNone } from '@/library/helper';
import InputField from '@/components/generic/input-field';
import ButtonField from '@/components/generic/button-field';
import CheckBoxField from '@/components/generic/checkbox-field';
import CountryInput from '@/components/generic/country-input';
import StateInput from '@/components/generic/state-input';
import PostalInput from '@/components/generic/postal-input';
import PhoneInput from '@/components/generic/phone-input';
import NameInput from '@/components/generic/name-input';
import { Collection, NotificationType } from '@/library/types';
import { state } from '@/library/api';
import { Templates } from '@/library/context';

export const DEFAULT_ADDRESS_CONTENT = {
    residential: false,
    country_code: Address.CountryCodeEnum.CA,
    state_code: 'QC'
} as Partial<Address>;

const NEXT_TAB_MAPPING: Collection = { "shipper": "recipient", "recipient": "parcel" };

interface AddressFormComponent {
    value?: Address;
    shipment?: Shipment;
    name: "shipper" | "recipient" | "template";
    update: (payload: {}, refresh?: boolean) => void;
}

function reducer(state: any, { name, value }: { name: string, value: string | boolean | object }) {
    switch (name) {
        case "full":
            return { ...(value as object) };
        case "partial":
            return { ...state, ...(value as object) };
        default:
            return { ...state, [name]: value };
    }
}


const AddressForm: React.FC<AddressFormComponent> = ({ value, shipment, name, update, children }) => {
    const form = useRef<HTMLFormElement>(null);
    const Defaults = useContext(Templates);
    const init = () => deepEqual(value, {}) ? DEFAULT_ADDRESS_CONTENT : value;
    const [key, setKey] = useState<string>(`address-${Date.now()}`);
    const [address, dispatch] = useReducer(reducer, value, init);
    const nextTab: string = NEXT_TAB_MAPPING[name];
    const handleChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        const target = event.target;
        const value = target.type === 'checkbox' ? target.checked : target.value;
        const name: string = target.name;

        dispatch({ name, value });
    };
    const handleSubmit = async (e: FormEvent) => {
        e.preventDefault();
        try {
            if (address.id !== undefined) {
                const udpated_address = await state.updateAddress(address);
                const changes = shipment?.id === undefined ? { [name]: udpated_address } : await state.retrieveShipment(shipment.id);
                state.setNotification({ type: NotificationType.success, message: name + ' Address successfully updated!' });
                update({ ...changes }, true);
            } else {
                update({ [name]: address });
                form.current?.dispatchEvent(
                    new CustomEvent('label-select-tab', { bubbles: true, detail: { nextTab, delay: 100 } })
                );
            }
            setKey(`address-${Date.now()}`);
        } catch (err) {
            state.setNotification({ type: NotificationType.error, message: err });
        }
    };

    useEffect(() => {
        if (shipment !== undefined && isNone(shipment.id) && name === "shipper" && !isNone(Defaults?.address) && !deepEqual(Defaults.address, address)) {
            dispatch({ name: "full", value: Defaults.address as Address });
        }
    }, [Defaults]);

    return (
        <form className="px-1 py-2" onSubmit={handleSubmit} key={key} ref={form}>

            {React.Children.map(children, (child: any) => React.cloneElement(child, { ...child.props, address, onChange: handleChange }))}

            <div className="columns mb-0">
                <NameInput label="name" onValueChange={(value, refresh) => { dispatch({ name: "partial", value }); refresh && setKey(`address-${Date.now()}`); }} defaultValue={address.person_name} disableSuggestion={isNone(shipment)} fieldClass="column mb-0 px-2 py-2" required />
            </div>

            <div className="columns mb-0">
                <InputField label="company" name="company_name" onChange={handleChange} defaultValue={address.company_name} fieldClass="column mb-0 px-2 py-2" />
            </div>

            <div className="columns mb-0">
                <InputField label="email" name="email" onChange={handleChange} defaultValue={address.email} fieldClass="column mb-0 is-7 px-2 py-2" type="email" />

                <PhoneInput label="phone" onValueChange={value => dispatch({ name: "phone_number", value: value as string })} defaultValue={address.phone_number} country={address.country_code} fieldClass="column mb-0 px-2 py-2" />
            </div>


            <div className="columns mb-0">
                <CountryInput label="country" onValueChange={value => dispatch({ name: "country_code", value: value as string })} defaultValue={address.country_code} fieldClass="column mb-0 px-2 py-2" required/>
            </div>

            <div className="columns mb-0">
                <InputField label="Street (Line 1)" name="address_line1" onChange={handleChange} defaultValue={address.address_line1} fieldClass="column mb-0 px-2 py-2" required />
            </div>

            <div className="columns is-multiline mb-0">
                <InputField label="Street (Line 2)" name="address_line2" onChange={handleChange} defaultValue={address.address_line2} fieldClass="column is-6 mb-0 px-2 py-2" />

                <InputField label="city" name="city" onChange={handleChange} defaultValue={address.city} fieldClass="column is-6 mb-0 px-2 py-2" />

                <StateInput label="province or state" onValueChange={value => dispatch({ name: "state_code", value: value as string })} defaultValue={address.state_code} country={address.country_code} fieldClass="column is-6 mb-0 px-2 py-2" />

                <PostalInput label="postal code" onValueChange={value => dispatch({ name: "postal_code", value: value as string })} defaultValue={address.postal_code} country={address.country_code} fieldClass="column is-6 mb-0 px-2 py-2" />
            </div>

            <div className="columns mb-0">

                <CheckBoxField name="residential" onChange={handleChange} defaultChecked={address.residential} fieldClass="column mb-0 is-12 px-2 py-2">
                    <span>Residential address</span>
                </CheckBoxField>

            </div>

            <ButtonField type="submit" className="is-primary" fieldClass="has-text-centered mt-3" disabled={deepEqual(value || {}, address)}>
                <span>{address.id === undefined ? 'Continue' : 'Save'}</span>
                {address.id === undefined && <span className="icon is-small">
                    <i className="fas fa-chevron-right"></i>
                </span>}
            </ButtonField>

        </form>
    )
};

export default AddressForm;