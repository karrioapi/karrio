import { Customs, Shipment } from '@purplship/purplship';
import React, { ChangeEvent, FormEvent, useRef, useState } from 'react';
import InputField from '@/components/generic/input-field';
import TextAreaField from '@/components/generic/textarea-field';
import CheckBoxField from '@/components/generic/checkbox-field';
import ButtonField from '@/components/generic/button-field';
import SelectField from '@/components/generic/select-field';
import DataInput from '@/components/generic/data-input';
import { Reference, User } from '@/library/context';
import { formatRef } from '@/library/helper';
import { Collection, CURRENCY_OPTIONS, PAYOR_OPTIONS } from '@/library/types';
import { NotificationType, state } from '@/library/api';


const DEFAULT_CUSTOMS: Customs = {
    content_type: Customs.ContentTypeEnum.Documents,
    certify: true,
    incoterm: Customs.IncotermEnum.DDU
};

interface ShipmentCustomsInfoComponent {
    shipment: Shipment;
    update: (payload: {}) => void;
}

const ShipmentCustomsInfo: React.FC<ShipmentCustomsInfoComponent> = ({ shipment, update }) => {
    const [customs, setCustoms] = useState<Customs>(shipment?.customs || DEFAULT_CUSTOMS);
    const [optOut, setOptOut] = useState<boolean>(!shipment.customs);
    const [hasDuty, setHasDuty] = useState<boolean>(!!shipment?.customs?.duty);
    const form = useRef<any>(null);
    const _ = (e: ChangeEvent<any> & CustomEvent<{ name: keyof Customs, value: object }>) => {
        e.stopPropagation();
        let payload = DEFAULT_CUSTOMS;
        if (e.detail !== undefined) {
            const property: keyof Customs = e.detail.name;
            payload = { [property]: { ...customs[property], ...e.detail.value } };
        } else {
            const property: keyof Customs = e.target.name;
            payload = { [property]: e.target.type === 'checkbox' ? e.target.checked : e.target.value };
        }

        let new_state = { ...customs, ...payload };
        if (!hasDuty) delete new_state.duty;
        setCustoms(new_state);
    };
    const handleSubmit = async (e: FormEvent) => {
        e.preventDefault();
        try {
            let data = { customs };
            if (customs.id !== undefined) {
                const updated_customs = await state.updateCustoms(customs);
                data = { customs: updated_customs };
                state.setNotification({ type: NotificationType.success, message: 'Customs Declaration successfully updated!' });
            }
            else if (shipment.id !== undefined) {
                const updated_customs = await state.addCustoms(shipment.id, customs);
                data = { customs: updated_customs };
                state.setNotification({ type: NotificationType.success, message: 'Customs Declaration added updated!' });
            }
            update(data);
            form.current?.dispatchEvent(new CustomEvent(
                'label-select-tab', { bubbles: true, detail: { nextTab: 'options' } }
            ));
        } catch (e) {
            state.setNotification({ type: NotificationType.error, message: e.message });
        }
    };
    const optOutChanged = async (e: ChangeEvent<any>) => {
        const optOut = e.target.checked;
        setHasDuty(false);
        try {
            if (customs.id !== undefined) {
                await state.discardCustoms(customs.id);
                state.setNotification({ type: NotificationType.success, message: 'Customs declaration discarded successfully!' });
            }
            update({ customs: undefined });
        } catch (e) {
            state.setNotification({ type: NotificationType.error, message: e.message });
        }
        setCustoms(optOut ? {} : DEFAULT_CUSTOMS);
    };

    form?.current?.addEventListener('change', _);

    return (
        <>
            <div className="columns is-multiline">
                <CheckBoxField defaultChecked={optOut} onChange={() => setOptOut(!optOut)} fieldClass="column mb-0 is-12 px-3 py-3 has-text-weight-semibold">
                    <span>Opt out of customs</span>
                </CheckBoxField>
            </div>

            {optOut && <div>
                <ButtonField className="is-primary" fieldClass="has-text-centered mt-3" onClick={optOutChanged} disabled={!shipment.customs}>
                    <span>Save</span>
                    <span className="icon is-small">
                        <i className="fas fa-chevron-right"></i>
                    </span>
                </ButtonField>
            </div>}

            {!optOut && <form className="px-1 py-2" onSubmit={handleSubmit} ref={form}>

                <div className="columns is-multiline mb-0">

                    <SelectField label="Content type" value={customs.content_type} name="content_type" className="is-fullwidth" fieldClass="column mb-0 is-6 px-2 py-1" required >
                        <Reference.Consumer>
                            {(ref) => (Object.values(ref || {}).length > 0) && Object
                                .entries(ref.customs_content_type as Collection)
                                .map(([code, name]) => (
                                    <option key={code} value={code}>{formatRef(name)}</option>
                                ))
                            }
                        </Reference.Consumer>
                    </SelectField>

                    <SelectField label="incoterm" value={customs.incoterm} name="incoterm" className="is-fullwidth" fieldClass="column mb-0 is-6 px-2 py-1" required >
                        <Reference.Consumer>
                            {(ref) => (Object.values(ref || {}).length > 0) && Object
                                .entries(ref.incoterms as Collection)
                                .map(([code, name]) => (
                                    <option key={code} value={code}>{`${code} (${name})`}</option>
                                ))
                            }
                        </Reference.Consumer>
                    </SelectField>

                    <InputField label="AES" defaultValue={customs.aes} name="aes" fieldClass="column mb-0 is-6 px-2 py-1" />

                    <InputField label="EEL / PFC" defaultValue={customs.eel_pfc} name="eel_pfc" fieldClass="column mb-0 is-6 px-2 py-1" />

                    <InputField label="certificate number" defaultValue={customs.certificate_number} name="certificate_number" fieldClass="column mb-0 is-6 px-2 py-1" />

                    <InputField label="invoice number" defaultValue={customs.invoice} name="invoice" fieldClass="column mb-0 is-6 px-2 py-1" />

                    <CheckBoxField defaultChecked={customs.commercial_invoice} name="commercial_invoice" fieldClass="column mb-0 is-12 px-2 py-2">
                        <span>Commercial Invoice</span>
                    </CheckBoxField>

                </div>

                <div className="columns is-multiline mb-0 pt-2">

                    <CheckBoxField defaultChecked={hasDuty} onChange={() => setHasDuty(!hasDuty)} fieldClass="column mb-0 is-12 px-2 py-2">
                        <span>Duties</span>
                    </CheckBoxField>

                    <DataInput state={customs.duty} onChange={_} className="columns column is-multiline mb-0 ml-6 my-1 px-2 py-0 is-12" style={{ borderLeft: "solid 2px #ddd", display: `${hasDuty ? 'block' : 'none'}` }}>

                        <SelectField label="paid by" value={customs.duty?.paid_by} name={'paid_by'} className="is-small is-fullwidth" fieldClass="column is-3 mb-0 px-1 py-2" required={hasDuty}>
                            <option value="">Select Payor</option>

                            {PAYOR_OPTIONS.map(unit => (
                                <option key={unit} value={unit}>{formatRef(unit)}</option>
                            ))}
                        </SelectField>

                        <SelectField label="prefered currency" value={customs.duty?.currency} name="currency" className="is-small is-fullwidth" fieldClass="column is-3 mb-0 px-1 py-2">
                            <option value="">Select a currency</option>

                            {CURRENCY_OPTIONS.map(unit => (
                                <option key={unit} value={unit}>{unit}</option>
                            ))}
                        </SelectField>

                    </DataInput>

                </div>

                <div className="columns is-multiline mb-0 pt-2">

                    <TextAreaField label="content description" defaultValue={customs.content_description} name="content_description" fieldClass="column mb-0 is-12 px-2 py-2" placeholder="Content type description" />

                    <User.Consumer>
                        {(user) => (
                            <InputField label="Signed By" defaultValue={(customs.signer || user.full_name) as string} name="signer" fieldClass="column mb-0 is-12 px-2 py-2" required />
                        )}
                    </User.Consumer>

                    <CheckBoxField defaultChecked={customs.certify} name="certify" fieldClass="column mb-0 is-12 px-2 py-2">
                        I certify this customs declaration.
                </CheckBoxField>

                </div>

                <ButtonField type="submit" className="is-primary" fieldClass="has-text-centered mt-3" disabled={shipment.customs == customs}>
                    <span>Save</span>
                    <span className="icon is-small">
                        <i className="fas fa-chevron-right"></i>
                    </span>
                </ButtonField>

            </form>}
        </>
    )
};

export default ShipmentCustomsInfo;