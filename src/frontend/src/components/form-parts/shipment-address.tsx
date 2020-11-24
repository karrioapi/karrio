import { Address, AddressData, Shipment } from '@purplship/purplship';
import React, { ChangeEvent, FormEvent, useState } from 'react';
import InputField from '@/components/generic/input-field';
import ButtonField from '@/components/generic/button-field';
import { Reference } from '@/library/context';
import { Collection } from '@/library/types';

interface ShipmentAddressComponent {
    shipment: Shipment;
    addressName: "shipper" | "recipient";
    update: (payload: {}) => void;
}

const ShipmentAddress: React.FC<ShipmentAddressComponent> = ({ shipment, addressName, update }) => {
    const [address, setAddress] = useState<Address>(shipment[addressName] || {});
    const nextTab: string = {
        "shipper": "recipient",
        "recipient": "parcel"
    }[addressName];
    const _ = (property: keyof AddressData) => (e: ChangeEvent<HTMLInputElement>) => {
        setAddress({ ...address, [property]: e.target.value });
    };
    const handleSubmit = (e: FormEvent) => {
        e.preventDefault();
        update({ [addressName]: address });
        e.currentTarget.dispatchEvent(new CustomEvent(
            'label-select-tab', { bubbles: true, detail: { nextTab } }
        ));
    };

    return (
        <form className="px-1 py-2" onSubmit={handleSubmit}>

            <div className="columns mb-0">
                <InputField label="name" onChange={_('person_name')} defaultValue={address!.person_name} fieldClass="column mb-0 px-2 py-2" required />

                <InputField label="company" onChange={_('company_name')} defaultValue={address!.company_name} fieldClass="column mb-0 px-2 py-2" />
            </div>

            <div className="columns mb-0">
                <InputField label="email" onChange={_('email')} defaultValue={address!.email} fieldClass="column mb-0 px-2 py-2" type="email" />

                <InputField label="phone" onChange={_('phone_number')} defaultValue={address!.phone_number} fieldClass="column mb-0 px-2 py-2" />
            </div>


            <h6 className="is-size-7 my-2 has-text-weight-semibold">Address</h6>


            <div className="columns mb-0">
                <InputField label="Street (Line 1)" onChange={_('address_line1')} defaultValue={address!.address_line1} fieldClass="column mb-0 px-2 py-2" required />

                <InputField label="Street (Line 2)" onChange={_('address_line2')} defaultValue={address!.address_line2} fieldClass="column mb-0 px-2 py-2" />
            </div>

            <div className="columns mb-0">
                <InputField label="city" onChange={_('city')} defaultValue={address!.city} fieldClass="column mb-0 px-2 py-2" />

                <InputField label="state or province" name="state" onChange={_('state_code')} defaultValue={address!.state_code} list="state_or_provinces" fieldClass="column mb-0 px-2 py-2">
                    <datalist id="state_or_provinces">
                        <Reference.Consumer>
                            {(ref) => (Object.values(ref || {}).length > 0) && Object
                                .entries(ref.states)
                                .map(([key, value]) => {
                                    return (
                                        <optgroup key={key} label={key}>
                                            {Object.entries(value as object).map(([state, name]) => (
                                                <option key={state} value={state}>{name}</option>
                                            ))}
                                        </optgroup>
                                    );
                                })
                            }
                        </Reference.Consumer>
                    </datalist>
                </InputField>

                <InputField label="country (code)" name="country" onChange={_('country_code')} defaultValue={address!.country_code} list="countries" fieldClass="column mb-0 px-2 py-2">
                    <datalist id="countries">
                        <Reference.Consumer>
                            {(ref) => (Object.values(ref || {}).length > 0) && Object
                                .entries(ref.countries as Collection)
                                .map(([code, name]) => (
                                    <option key={code} value={code}>{name}</option>
                                ))
                            }
                        </Reference.Consumer>
                    </datalist>
                </InputField>

                <InputField label="postal code" onChange={_('postal_code')} defaultValue={address!.postal_code} fieldClass="column mb-0 px-2 py-2" />
            </div>

            <ButtonField type="submit" className="is-primary" fieldClass="has-text-centered mt-3" disabled={shipment[addressName] == address}>
                <span>Save</span>
                <span className="icon is-small">
                    <i className="fas fa-chevron-right"></i>
                </span>
            </ButtonField>

        </form>
    )
};

export default ShipmentAddress;