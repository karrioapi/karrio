import React, { EventHandler, useContext, useState } from 'react';
import { Shipment, Address } from '@/api';
import AddressForm from '@/components/form-parts/address-form';
import { isNone } from '@/library/helper';
import InputField from '@/components/generic/input-field';
import CheckBoxField from './generic/checkbox-field';
import { AddressTemplate, NotificationType } from '@/library/types';
import TemplateMutation from '@/components/data/template-mutation';
import { Notify } from './notifier';

const DEFAULT_TEMPLATE_CONTENT = {
    address: {
        residential: false,
        country_code: 'CA',
        state_code: 'QC'
    }
} as AddressTemplate;

type ExtendedAddress = AddressTemplate['address'] & { label: string; is_default?: boolean; };
type ExtendedShipment = Shipment & { template: ExtendedAddress; };

interface AddressEditModalComponent {
    addressTemplate?: AddressTemplate;
    className: string;
    onUpdate?: () => void;
}

const AddressEditModal: React.FC<AddressEditModalComponent> = TemplateMutation<AddressEditModalComponent>(
    ({ addressTemplate, onUpdate, children, className, createTemplate, updateTemplate }) => {
        const { notify } = useContext(Notify);
        const [isActive, setIsActive] = useState<boolean>(false);
        const [key, setKey] = useState<string>(`address-${Date.now()}`);
        const [isNew, _] = useState<boolean>(isNone(addressTemplate));
        const [payload, setPayload] = useState<ExtendedAddress | undefined>();

        const open = () => {
            setIsActive(true);
            const { label, is_default, address } = addressTemplate || DEFAULT_TEMPLATE_CONTENT;

            setPayload({ ...address, label, is_default } as ExtendedAddress);
        };
        const close = (_?: React.MouseEvent, changed?: boolean) => {
            if (isNew) setPayload(undefined);
            if (changed && onUpdate !== undefined) onUpdate();
            setIsActive(false);
            setKey(`address-${Date.now()}`);
        };
        const update = async ({ changes }: any) => {
            const { label, is_default, ...address } = (changes as ExtendedShipment).template;
            if (isNew) {
                await createTemplate({ label, is_default, address: address });
                notify({ type: NotificationType.success, message: 'Address successfully added!' });
            }
            else {
                await updateTemplate({ label, is_default, address: address, id: addressTemplate?.id as string });
                notify({ type: NotificationType.success, message: 'Address successfully updated!' });
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
                            {payload !== undefined && <AddressForm value={payload as any} name="template" update={update}>

                                <Extension />

                            </AddressForm>}
                        </form>

                    </div>

                    <button className="modal-close is-large" aria-label="close" onClick={close}></button>
                </div>
            </>
        )
    });

export default AddressEditModal;