import React, { EventHandler, useContext, useState } from 'react';
import { isNone } from '@/library/helper';
import CustomsInfoForm from '@/components/form-parts/customs-info-form';
import InputField from '@/components/generic/input-field';
import { CustomsTemplateType, CustomsType, NotificationType } from '@/library/types';
import TemplateMutation from '@/components/data/template-mutation';
import CheckBoxField from '@/components/generic/checkbox-field';
import { Notify } from './notifier';

const DEFAULT_TEMPLATE_CONTENT = {
    customs: {
        certify: true,
        incoterm: 'DDU',
        content_type: 'merchandise',
    }
} as CustomsTemplateType;

type ExtendedCustoms = CustomsType & { label: string; is_default?: boolean; };
interface CustomsInfoEditModalComponent {
    customsTemplate?: CustomsTemplateType;
    className: string;
    onUpdate?: () => void;
}

const CustomsInfoEditModal: React.FC<CustomsInfoEditModalComponent> = TemplateMutation<CustomsInfoEditModalComponent>(
    ({ customsTemplate, onUpdate, children, className, createTemplate, updateTemplate }) => {
        const { notify } = useContext(Notify);
        const [isActive, setIsActive] = useState<boolean>(false);
        const [key, setKey] = useState<string>(`customs-${Date.now()}`);
        const [isNew, _] = useState<boolean>(isNone(customsTemplate));
        const [payload, setPayload] = useState<CustomsType | undefined>();

        const open = () => {
            setIsActive(true);
            const { label, is_default, customs } = customsTemplate || DEFAULT_TEMPLATE_CONTENT;

            setPayload({ ...customs, is_default, label } as ExtendedCustoms);
        };
        const close = (_?: React.MouseEvent, changed?: boolean) => {
            if (isNew) setPayload(undefined);
            if (changed && onUpdate !== undefined) onUpdate();
            setIsActive(false);
            setKey(`customs-${Date.now()}`);
        };
        const update = async ({ changes }: any) => {
            const { label, is_default, ...data } = (changes as { customs: ExtendedCustoms }).customs;
            if (isNew) {
                await createTemplate({ label, is_default, customs: data as any   });
                notify({ type: NotificationType.success, message: 'Customs info successfully added!' });
            }
            else {
                await updateTemplate({ label, is_default, customs: data as any, id: customsTemplate?.id as string });
                notify({ type: NotificationType.success, message: 'Customs info successfully updated!' });
            }

            close(undefined, true);
        };
        const Extension: React.FC<{ onChange?: EventHandler<any>; customs?: ExtendedCustoms }> = ({ onChange, customs }) => (
            <>
                <div className="columns mb-2">
                    <InputField label="label" name="label" onChange={onChange} defaultValue={customs?.label} fieldClass="column mb-0 px-2 py-2" required />
                </div>

                <div className="columns mb-1">
                    <CheckBoxField name="is_default" onChange={onChange} defaultChecked={customs?.is_default} fieldClass="column mb-0 px-2 py-2">
                        <span>Set as default customs info</span>
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
                            <h3 className="subtitle is-3">{isNew ? 'New' : 'Update'} Customs Info</h3>
                            <hr />
                            {payload !== undefined && <CustomsInfoForm value={payload as any} update={update} cannotOptOut={true}>
                                <Extension />
                            </CustomsInfoForm>}
                        </section>

                    </div>

                    <button className="modal-close is-large" aria-label="close" onClick={close}></button>
                </div>
            </>
        )
    });

export default CustomsInfoEditModal;