import { state } from '@/library/api';
import { NotificationType } from '@/library/types';
import React, { useState } from 'react';

interface GenerateAPIModalComponent {}

const GenerateAPIModal: React.FC<GenerateAPIModalComponent> = ({ children }) => {
    const [password, setPassword] = useState<string>("");
    const [error, setError] = useState<string>("");
    const [isActive, setIsActive] = useState<boolean>(false);
    const [isDisabled, setIsDisabled] = useState<boolean>(false);
    const [hasError, setHasError] = useState<boolean>(false);
    const handleSubmit = async (evt: React.FormEvent<HTMLFormElement>) => {
        evt.preventDefault();
        try {
            setIsDisabled(true);
            await state.regenerateToken(password);
            setPassword("");
            setIsDisabled(false);
            setIsActive(false);
            setHasError(false);
            state.setNotification({ 
                type: NotificationType.success,
                message: "New token generated successfully!"
            });
        } catch(err) {
            setError(err.message);
            setIsDisabled(false);
            setHasError(true);
        }
    };
    const close = (evt: React.MouseEvent) => {
        evt.preventDefault();
        setPassword("");
        setIsDisabled(false);
        setIsActive(false);
        setHasError(false);
    }

    return (
        <>
            <button className="button is-primary is-small" onClick={() => setIsActive(true)}>
                {children}
            </button>

            <div className={`modal ${isActive ? "is-active" : ""}`}>
                <div className="modal-background" onClick={close}></div>
                <form className="modal-card" onSubmit={handleSubmit}>
                    <section className="modal-card-body">
                        <div className="field">
                            <label className="label">Enter your password</label>
                            <div className="control">
                                <input
                                    className="input is-small"
                                    type="password"
                                    onChange={e => setPassword(e.target.value)}
                                    value={password}
                                    disabled={isDisabled}
                                    required />
                            </div>
                            <p className="is-size-7 has-text-danger my-1" style={{ visibility: (hasError ? "visible" : "hidden")}}>{error}</p>
                            <input className="button is-small is-fullwidth mt-2" type="submit" value="Submit" disabled={isDisabled} />
                        </div>
                    </section>
                </form>
                <button className="modal-close is-large" aria-label="close" onClick={close}></button>
            </div>
        </>
    )
};

export default GenerateAPIModal;