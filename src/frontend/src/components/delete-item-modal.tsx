import { NotificationType, state } from '@/library/api';
import React, { useState } from 'react';

interface DeleteItemModalComponent {
    identifier: string;
    label: string;
    onConfirm: () => Promise<void>;
}

const DeleteItemModal: React.FC<DeleteItemModalComponent> = ({ identifier, label, onConfirm, children }) => {
    const [isActive, setIsActive] = useState<boolean>(false);

    const close = (evt?: React.MouseEvent) => {
        evt?.preventDefault();
        setIsActive(false);
    };
    const handleSubmit = async (evt: React.FormEvent<HTMLFormElement>) => {
        evt.preventDefault();
        try {
            await onConfirm();
            state.setNotification({ 
                type: NotificationType.success, message: `${label} deteled successfully!...`
            });
            close();
        } catch(message) {
            state.setNotification({ type: NotificationType.error, message });
        }
    };

    return (
        <>
            <button className="button is-danger is-light" onClick={() => setIsActive(true)}>
                {children}
            </button>

            <div className={`modal ${isActive ? "is-active" : ""}`}>
                <div className="modal-background" onClick={close}></div>
                <form className="modal-card" onSubmit={handleSubmit}>
                    <section className="modal-card-body">
                        <h3 className="subtitle is-3">Delete {label} <span className="is-size-7">({identifier})</span></h3>

                        <div className="buttons my=2">
                            <button className="button is-info is-light" onClick={close}>Cancel</button>
                            <input className="button is-danger" type="submit" value="Delete"/>
                        </div>
                    </section>
                </form>
                <button className="modal-close is-large" aria-label="close" onClick={close}></button>
            </div>
        </>
    )
};

export default DeleteItemModal;