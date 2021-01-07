import React, { EventHandler, useState } from 'react';
import { Parcel } from '@purplship/purplship';
import ParcelForm, { DEFAULT_PARCEL_CONTENT } from '@/components/form-parts/parcel-form';
import { isNone } from '@/library/helper';
import InputField from './generic/input-field';
import CheckBoxField from './generic/checkbox-field';
import { NotificationType, Template } from '@/library/types';
import { state } from '@/library/api';

const DEFAULT_TEMPLATE_CONTENT = {
    parcel: DEFAULT_PARCEL_CONTENT
} as Template;

type ExtendedParcel = Parcel & { label?: string; is_default?: boolean; };

interface ParcelEditModalComponent {
    parcelTemplate?: Template;
    className: string;
    onUpdate?: () => void;
}

const ParcelEditModal: React.FC<ParcelEditModalComponent> = ({ parcelTemplate, onUpdate, children, className }) => {
    const [isActive, setIsActive] = useState<boolean>(false);
    const [key, setKey] = useState<string>(`parcel-${Date.now()}`);
    const [isNew, _] = useState<boolean>(isNone(parcelTemplate));
    const [payload, setPayload] = useState<Parcel | undefined>();

    const open = () => {
        setIsActive(true);
        const { label, is_default, parcel } = parcelTemplate || DEFAULT_TEMPLATE_CONTENT;
        const { id, ...parcel_content } = parcel as Parcel;

        setPayload({ ...parcel_content, is_default, label } as ExtendedParcel);
    };
    const close = (_?: React.MouseEvent, changed?: boolean) => {
        if (isNew) setPayload(undefined);
        if (changed && onUpdate !== undefined) onUpdate();
        setIsActive(false);
        setKey(`parcel-${Date.now()}`);
    };
    const update = async (changes: {}, ..._: any[]) => {
        const { label, is_default, ...parcel } = (changes as { parcels: ExtendedParcel[] }).parcels[0];
        if (isNew) {
            await state.saveTemplate({ label, is_default, parcel });
            state.setNotification({ type: NotificationType.success, message: 'Parcel successfully added!' });
        }
        else {
            await state.updateTemplate(parcelTemplate?.id as string, { label, is_default, parcel });
            state.setNotification({ type: NotificationType.success, message: 'Parcel successfully updated!' });
        }

        close(undefined, true);
    };
    const Extension: React.FC<{ onChange?: EventHandler<any>; parcel?: ExtendedParcel }> = ({ onChange, parcel }) => (
        <>
            <div className="columns mb-0">
                <InputField label="label" name="label" onChange={onChange} defaultValue={parcel?.label} fieldClass="column mb-0 px-2 py-2" required />
            </div>
            <div className="columns mb-1">
                <CheckBoxField name="is_default" onChange={onChange} defaultChecked={parcel?.is_default} fieldClass="column mb-0 px-2 py-2">
                    <span>Set as default parcel</span>
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

                    <section className="modal-card-body">
                        <h3 className="subtitle is-3">{isNew ? 'New' : 'Update'} Parcel</h3>
                        <hr />
                        {payload !== undefined && <ParcelForm value={payload} update={update}>
                            <Extension />
                        </ParcelForm>}
                    </section>

                </div>

                <button className="modal-close is-large" aria-label="close" onClick={close}></button>
            </div>
        </>
    )
};

export default ParcelEditModal;