import React, { EventHandler, useState } from 'react';
import { Customs } from '@purplship/purplship';
import { isNone } from '@/library/helper';
import { NotificationType, state, Template } from '@/library/api';
import CustomsInfoForm, { DEFAULT_CUSTOMS_CONTENT } from './form-parts/customs-info-form';
import InputField from '@/components/generic/input-field';

const DEFAULT_TEMPLATE_CONTENT = {
    customs: DEFAULT_CUSTOMS_CONTENT
} as Template;

type ExtendedCustoms = Customs & { label?: string; };
interface CustomsInfoEditModalComponent {
    customsTemplate?: Template;
    className: string;
    onUpdate?: () => void;
}

const CustomsInfoEditModal: React.FC<CustomsInfoEditModalComponent> = ({ customsTemplate, onUpdate, children, className }) => {
    const [isActive, setIsActive] = useState<boolean>(false);
    const [key, setKey] = useState<string>(`customs-${Date.now()}`);
    const [isNew, _] = useState<boolean>(isNone(customsTemplate));
    const [payload, setPayload] = useState<Customs | undefined>();

    const open = () => {
        setIsActive(true);
        const { label, customs } = customsTemplate || DEFAULT_TEMPLATE_CONTENT;
        const { id, ...customs_content } = customs as Customs;

        setPayload({ ...customs_content, label } as ExtendedCustoms);
    };
    const close = (_?: React.MouseEvent, changed?: boolean) => {
        if (isNew) setPayload(undefined);
        if (changed && onUpdate !== undefined) onUpdate();
        setIsActive(false);
        setKey(`customs-${Date.now()}`);
    };
    const update = async (changes: {}, ..._: any[]) => {
        const { label, ...customs } = (changes as { customs: ExtendedCustoms }).customs;
        if (isNew) {
            await state.saveTemplate({ label, customs });
            state.setNotification({ type: NotificationType.success, message: 'Customs info successfully added!' });
        }
        else {
            await state.updateTemplate(customsTemplate?.id as string, { label, customs });
            state.setNotification({ type: NotificationType.success, message: 'Customs info successfully updated!' });
        }

        close(undefined, true);
    };
    const Extension: React.FC<{ onChange?: EventHandler<any>; customs?: ExtendedCustoms }> = ({ onChange, customs }) => (
        <div className="columns mb-0">
            <InputField label="label" name="label" onChange={onChange} defaultValue={customs?.label} fieldClass="column mb-0 px-2 py-2" required />
        </div>
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
                        <h3 className="subtitle is-3">{isNew ? 'New' : 'Update'} Customs Info</h3>
                        <hr />
                        {payload !== undefined && <CustomsInfoForm value={payload} update={update} cannotOptOut={true}>
                            <Extension />    
                        </CustomsInfoForm>}
                    </section>

                </div>

                <button className="modal-close is-large" aria-label="close" onClick={close}></button>
            </div>
        </>
    )
};

export default CustomsInfoEditModal;