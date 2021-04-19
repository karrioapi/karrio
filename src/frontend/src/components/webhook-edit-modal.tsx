import React, { useContext, useState } from 'react';
import { NotificationType } from '@/library/types';
import ButtonField from '@/components/generic/button-field';
import WebhookMutation from './data/webhook-mutation';
import { Webhook, WebhookData, WebhookDataEnabledEventsEnum } from '@/api';
import { Notify } from './notifier';

interface WebhookEditModalComponent {
    webhook?: Webhook;
    className?: string;
}
const DEFAULT_STATE = {} as (Webhook | WebhookData);

const WebhookEditModal: React.FC<WebhookEditModalComponent> = WebhookMutation<WebhookEditModalComponent>(
    ({ webhook, children, className, addWebhook, updateWebhook }) => {
        const { notify } = useContext(Notify);
        const [isActive, setIsActive] = useState<boolean>(false);
        const [key, setKey] = useState<string>(`webhook-${Date.now()}`);
        const [isNew, _] = useState<boolean>(webhook === null || webhook === undefined);
        const [payload, setPayload] = useState<Webhook | WebhookData>(webhook || DEFAULT_STATE);
        const [isDisabled, setIsDisabled] = useState<boolean>(true);

        const close = (_?: React.MouseEvent) => {
            if (isNew) setPayload(DEFAULT_STATE as Webhook);
            setKey(`webhook-${Date.now()}`);
            setIsDisabled(false);
            setIsActive(false);
        };
        const handleSubmit = async (evt: React.FormEvent<HTMLFormElement>) => {
            evt.preventDefault();
            try {
                setIsDisabled(true);
                if (isNew) {
                    await addWebhook(payload as WebhookData);
                } else {
                    await updateWebhook(payload as Webhook);
                }
                notify({
                    type: NotificationType.success,
                    message: `carrier connection ${isNew ? 'registered' : 'updated'} successfully`
                });
                close();
            } catch (err) {
                notify({ type: NotificationType.error, message: err });
                setIsDisabled(false);
            }
        };

        return (
            <>
                <button className={className} onClick={() => setIsActive(true)}>
                    {children}
                </button>

                <div className={`modal ${isActive ? "is-active" : ""}`} key={key}>
                    <div className="modal-background" onClick={close}></div>
                    <form className="modal-card" onSubmit={handleSubmit}>
                        <section className="modal-card-body">
                            <h3 className="subtitle is-3">{isNew ? 'Add a Webhook' : 'Update a Webhook'}</h3>



                            <ButtonField
                                type="submit"
                                className="is-primary"
                                fieldClass="has-text-centered mt-6"
                                disabled={isDisabled}>
                                <span>Submit</span>
                            </ButtonField>
                        </section>
                    </form>
                    <button className="modal-close is-large" aria-label="close" onClick={close}></button>
                </div>
            </>
        )
    });

export default WebhookEditModal;