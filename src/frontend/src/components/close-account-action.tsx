import { NotificationType, state } from '@/library/api';
import React, { useState } from 'react';

interface CloseAccountActionComponent {

}

const CloseAccountAction: React.FC<CloseAccountActionComponent> = ({ children }) => {
    const [isActive, setIsActive] = useState<boolean>(false);
    const close = (evt: React.MouseEvent) => {
        evt.preventDefault();
        setIsActive(false);
    }
    const handleSubmit = async (evt: React.FormEvent<HTMLFormElement>) => {
        evt.preventDefault();
        try {
            await state.closeAccount();
        } catch(err) {
            state.setNotification({ type: NotificationType.error, message: err });
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
                        <h3 className="subtitle is-3">Close Account</h3>

                        <div className="buttons my=2">
                            <button className="button is-info is-light" onClick={close}>Cancel</button>
                            <input className="button is-danger" type="submit" value="Close My Account"/>
                        </div>
                    </section>
                </form>
                <button className="modal-close is-large" aria-label="close" onClick={close}></button>
            </div>
        </>
    )
};

export default CloseAccountAction;