import React, { EventHandler, useState } from 'react';
import { Address, Shipment } from '@/api';
import AddressForm, { DEFAULT_ADDRESS_CONTENT } from '@/components/form-parts/address-form';
import { isNone } from '@/library/helper';
import InputField from '@/components/generic/input-field';
import CheckBoxField from './generic/checkbox-field';
import { NotificationType, Template } from '@/library/types';
import { state } from '@/library/app';

const DEFAULT_TEMPLATE_CONTENT = {
    address: DEFAULT_ADDRESS_CONTENT
} as Template;

type ExtendedAddress = Address & { label: string; is_default?: boolean; };
type ExtendedShipment = Shipment & { template: ExtendedAddress; };

interface AddressEditModalComponent {
    addressTemplate?: Template;
    className: string;
    onUpdate?: () => void;
}

const AddressEditModal: React.FC<AddressEditModalComponent> = ({ addressTemplate, onUpdate, children, className }) => {
    const [isActive, setIsActive] = useState<boolean>(false);
    const [key, setKey] = useState<string>(`address-${Date.now()}`);
    const [isNew, _] = useState<boolean>(isNone(addressTemplate));
    const [payload, setPayload] = useState<ExtendedAddress | undefined>();

    const open = () => {
        setIsActive(true);
        const { label, is_default, address } = addressTemplate || DEFAULT_TEMPLATE_CONTENT;
        const { id, ...address_content } = address as Address;

        setPayload({ ...address_content, label, is_default } as ExtendedAddress);
    };
    const close = (_?: React.MouseEvent, changed?: boolean) => {
        if (isNew) setPayload(undefined);
        if (changed && onUpdate !== undefined) onUpdate();
        setIsActive(false);
        setKey(`address-${Date.now()}`);
    };
    const update = async (changes: {}, ..._: any[]) => {
        const { label, is_default, ...address } = (changes as ExtendedShipment).template;
        if (isNew) {
            await state.saveTemplate({ label, is_default, address });
            state.setNotification({ type: NotificationType.success, message: 'Address successfully added!' });
        }
        else {
            await state.updateTemplate(addressTemplate?.id as string, { label, is_default, address });
            state.setNotification({ type: NotificationType.success, message: 'Address successfully updated!' });
        }

        close(undefined, true);
    };
    const Extension: React.FC<{ onChange?: EventHandler<any>; address?: ExtendedAddress }> = ({ onChange, address }) => (
        <>
            <div className="columns mb-0">
                <InputField label="label" name="label" onChange={onChange} defaultValue={address?.label} fieldClass="column mb-0 px-2 py-2" required />
            </div>
            <div className="columns mb-1">
                <CheckBoxField name="is_default" onChange={onChange} defaultChecked={address?.is_default} fieldClass="column mb-0 px-2 py-2">
                    <span>Set as default address</span>
                </CheckBoxField>
            </div>
        </>
    );

    return (
        <>
            <button className={className} onClick={open}>
                {children}
            </button>

            <div className={`modal ${isActive ? "is-active" : ""}`} key={key}>
                <div className="modal-background" onClick={close}></div>
                <div className="modal-card">

                    <form className="modal-card-body">
                        <h3 className="subtitle is-3">{isNew ? 'New' : 'Update'} Address</h3>
                        <hr />
                        {payload !== undefined && <AddressForm value={payload} name="template" update={update}>

                            <Extension />

                        </AddressForm>}
                    </form>

                </div>

                <button className="modal-close is-large" aria-label="close" onClick={close}></button>
            </div>
        </>
    )
};

export default AddressEditModal;