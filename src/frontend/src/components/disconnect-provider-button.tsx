import { NotificationType } from '@/library/types';
import React, { useContext, useState } from 'react';
import ConnectionMutation from './data/connection-mutation';
import { UserConnectionType } from './data/user-connections-query';
import { Notify } from './notifier';

interface DisconnectProviderButtonComponent {
    connection: UserConnectionType;
}

const DisconnectProviderButton: React.FC<DisconnectProviderButtonComponent> = ConnectionMutation<DisconnectProviderButtonComponent>(
    ({ children, connection, deleteConnection }) => {
        const { notify } = useContext(Notify);
        const [isActive, setIsActive] = useState<boolean>(false);
        const close = (evt?: React.MouseEvent) => {
            evt?.preventDefault();
            setIsActive(false);
        };
        const handleSubmit = async (evt: React.FormEvent<HTMLFormElement>) => {
            evt.preventDefault();
            try {
                await deleteConnection(connection.id as string);
                notify({
                    type: NotificationType.success,
                    message: 'Carrier account disconnected successfully!'
                });
                close();
            } catch (err) {
                notify({ type: NotificationType.error, message: err });
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
                            <h3 className="subtitle is-3">Disconnect Carrier ({connection.carrier_id})</h3>

                            <div className="buttons my=2">
                                <button className="button is-info is-light" onClick={close}>Cancel</button>
                                <input className="button is-danger" type="submit" value="Disconnect" />
                            </div>
                        </section>
                    </form>
                    <button className="modal-close is-large" aria-label="close" onClick={close}></button>
                </div>
            </>
        )
    });

export default DisconnectProviderButton;