import { Provider, state } from '@/library/api';
import React, { useState } from 'react';

interface DisconnectProviderButtonComponent {
    provider: Provider;
}

const DisconnectProviderButton: React.FC<DisconnectProviderButtonComponent> = ({ children, provider }) => {
    const [isActive, setIsActive] = useState<boolean>(false);
    const close = (evt?: React.MouseEvent) => {
        evt?.preventDefault();
        setIsActive(false);
    }
    const handleSubmit = async (evt: React.FormEvent<HTMLFormElement>) => {
        evt.preventDefault();
        await state.disconnectProvider(provider.id as string);
        close();
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
                        <h3 className="subtitle is-3">Disconnect Carrier ({provider.carrierId})</h3>

                        <div className="buttons my=2">
                            <button className="button is-info is-light" onClick={close}>Cancel</button>
                            <input className="button is-danger" type="submit" value="Disconnect"/>
                        </div>
                    </section>
                </form>
                <button className="modal-close is-large" aria-label="close" onClick={close}></button>
            </div>
        </>
    )
};

export default DisconnectProviderButton;