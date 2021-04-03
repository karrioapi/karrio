import React, { EventHandler, useContext, useState } from 'react';
import ParcelForm from '@/components/form-parts/parcel-form';
import { isNone } from '@/library/helper';
import InputField from '@/components/generic/input-field';
import CheckBoxField from '@/components/generic/checkbox-field';
import { NotificationType, ParcelTemplateType, ParcelType } from '@/library/types';
import TemplateMutation from '@/components/data/template-mutation';
import { Notify } from '@/components/notifier';

const DEFAULT_TEMPLATE_CONTENT = {
    parcel: {
        packaging_type: "envelope",
        weight_unit: 'KG',
        dimension_unit: 'CM'
    }
} as ParcelTemplateType;

type ExtendedParcel = ParcelType & { label?: string; is_default?: boolean; };

interface ParcelEditModalComponent {
    parcelTemplate?: ParcelTemplateType;
    className: string;
    onUpdate?: () => void;
}

const ParcelEditModal: React.FC<ParcelEditModalComponent> = TemplateMutation<ParcelEditModalComponent>(
    ({ parcelTemplate, onUpdate, children, className, createTemplate, updateTemplate }) => {
        const { notify } = useContext(Notify);
        const [isActive, setIsActive] = useState<boolean>(false);
        const [key, setKey] = useState<string>(`parcel-${Date.now()}`);
        const [isNew, _] = useState<boolean>(isNone(parcelTemplate));
        const [payload, setPayload] = useState<ParcelType | undefined>();

        const open = () => {
            setIsActive(true);
            const { label, is_default, parcel } = parcelTemplate || DEFAULT_TEMPLATE_CONTENT;

            setPayload({ ...parcel, is_default, label } as ExtendedParcel);
        };
        const close = (_?: React.MouseEvent, changed?: boolean) => {
            if (isNew) setPayload(undefined);
            if (changed && onUpdate !== undefined) onUpdate();
            setIsActive(false);
            setKey(`parcel-${Date.now()}`);
        };
        const update = async ({ changes }: any) => {
            const { label, is_default, ...parcel } = (changes as { parcels: ExtendedParcel[] }).parcels[0];
            if (isNew) {
                await createTemplate({ label, is_default, parcel: parcel as any });
                notify({ type: NotificationType.success, message: 'Parcel successfully added!' });
            }
            else {
                await updateTemplate({ label, is_default, id: parcelTemplate?.id as string, parcel: parcel as any });
                notify({ type: NotificationType.success, message: 'Parcel successfully updated!' });
            }

            close(undefined, true);
        };
        const Extension: React.FC<{ onChange?: EventHandler<any>; parcel?: ExtendedParcel }> = ({ onChange, parcel }) => (
            <>
                <div className="columns mb-0 px-2">
                    <InputField label="label" name="label" onChange={onChange} defaultValue={parcel?.label} fieldClass="column mb-0 px-2 py-2" required />
                </div>
                <div className="columns mb-1 px-2">
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
                            {payload !== undefined && <ParcelForm value={payload as any} update={update}>
                                <Extension />
                            </ParcelForm>}
                        </section>

                    </div>

                    <button className="modal-close is-large" aria-label="close" onClick={close}></button>
                </div>
            </>
        )
    });

export default ParcelEditModal;