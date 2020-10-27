import { Connection, state } from '@/library/api';
import { CarrierSettings } from '@purplship/purplship';
import React, { useState } from 'react';
import { Reference } from '@/library/context';

interface ConnectProviderModalComponent {
    connection?: Connection;
    className?: string;
}

const ConnectProviderModal: React.FC<ConnectProviderModalComponent> = ({ children, connection, className }) => {
    const [key, setKey] = useState<string>(`connection-${Date.now()}`);
    const [isNew, _] = useState<boolean>(connection === null || connection === undefined);
    const [payload, setPayload] = useState<Partial<Connection>>(connection || { carrier_name: 'none' });
    const [error, setError] = useState<string>("");
    const [isActive, setIsActive] = useState<boolean>(false);
    const [isDisabled, setIsDisabled] = useState<boolean>(true);
    const [hasError, setHasError] = useState<boolean>(false);

    const handleSubmit = async (evt: React.FormEvent<HTMLFormElement>) => {
        evt.preventDefault();
        try {
            setIsDisabled(true);
            const data = {
                carrier_name: payload.carrier_name as CarrierSettings.CarrierNameEnum,
                carrier_config: payload
            };
            if (isNew) {
                await state.connectProvider(data);
            } else {
                const response = await state.updateConnection(payload.id as string, data);
                setPayload(response);
            }
            close();
        } catch (err) {
            setHasError(true);
            setError(err.message);
            setIsDisabled(false);
        }
    };
    const close = (_?: React.MouseEvent) => {
        if(isNew) setPayload({ carrier_name: 'none' });
        setKey(`connection-${Date.now()}`);
        setHasError(false);
        setIsDisabled(false);
        setIsActive(false);
    }
    const handleOnChange = (property: string) => (e: React.ChangeEvent<any>) => {
        let new_state = { ...payload, [property]: e.target.value || undefined };
        if (property === 'carrier_name') {
            setKey(`connection-${Date.now()}`);
            new_state = { carrier_name: e.target.value };
        } else if(property == 'test') {
            new_state = { ...payload, test: e.target.checked };
        }
        setPayload(new_state);
        setIsDisabled((connection || { carrier_name: 'none' }) == new_state);
    };
    const has = (property: string) => {
        return hasProperty(payload.carrier_name as CarrierSettings.CarrierNameEnum, property);
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
                        <h3 className="subtitle is-3">Connect a Carrier</h3>
                        <p className="is-size-7 has-text-danger my-1" style={{ visibility: (hasError ? "visible" : "hidden") }}>{error}</p>

                        <div className="field">
                            <div className="select is-fullwidth">
                                <select defaultValue={payload.carrier_name} onChange={handleOnChange("carrier_name")} disabled={!isNew} key={`select-${key}`} required>
                                    <option value='none'>Select Carrier</option>

                                    <Reference.Consumer>
                                        {(ref) => (Object.values(ref || {}).length > 0) && Object.keys(ref.carriers).map(carrier => (
                                            <option key={carrier} value={carrier}>{ref.carriers[carrier]}</option>
                                        ))}
                                    </Reference.Consumer>

                                </select>
                            </div>
                        </div>

                        {(payload.carrier_name !== 'none' && has("carrier_id")) &&
                            <>
                                <hr />

                                <FormInput label="Carrier Id" defaultValue={payload.carrier_id} onChange={handleOnChange("carrier_id")} required />

                                {/* Carrier specific fields BEGING */}

                                {has("site_id") && <FormInput label="Site Id" defaultValue={payload.site_id} onChange={handleOnChange("site_id")} required />}

                                {has("username") && <FormInput label="Username" defaultValue={payload.username} onChange={handleOnChange("username")} required />}

                                {has("password") && <FormInput label="Password" defaultValue={payload.password} onChange={handleOnChange("password")} required />}

                                {has("customer_number") && <FormInput label="Customer Number" defaultValue={payload.customer_number} onChange={handleOnChange("customer_number")} required />}

                                {has("contract_id") && <FormInput label="Contract Id" defaultValue={payload.contract_id} onChange={handleOnChange("contract_id")} />}

                                {has("account_number") && <FormInput label="Account Number" defaultValue={payload.account_number} onChange={handleOnChange("account_number")} required />}

                                {has("user_key") && <FormInput label="User Key" defaultValue={payload.user_key} onChange={handleOnChange("user_key")} />}

                                {has("meter_number") && <FormInput label="Meter Number" defaultValue={payload.meter_number} onChange={handleOnChange("meter_number")} required />}

                                {has("user_token") && <FormInput label="User Token" defaultValue={payload.user_token} onChange={handleOnChange("user_token")} />}

                                {has("access_license_number") && <FormInput label="Access License Number" defaultValue={payload.access_license_number} onChange={handleOnChange("access_license_number")} required />}

                                {/* Carrier specific fields END */}

                                <div className="field">
                                    <div className="control">
                                        <label className="checkbox">
                                            <input type="checkbox" defaultChecked={payload.test} onChange={handleOnChange("test")} />
                                            <span>Test Mode</span>
                                        </label>
                                    </div>
                                </div>

                                <input className="button is-small is-fullwidth mt-2" type="submit" value="Submit" disabled={isDisabled} />
                            </>
                        }
                    </section>
                </form>
                <button className="modal-close is-large" aria-label="close" onClick={close}></button>
            </div>
        </>
    )
};

function hasProperty(carrier_name: CarrierSettings.CarrierNameEnum, property: string): boolean {
    // TODO: Use carriers settings types when available for automatic validation
    return ({
        [CarrierSettings.CarrierNameEnum.Canadapost]: ["carrier_id", "test", "username", "password", "customer_number", "contract_id"],
        [CarrierSettings.CarrierNameEnum.DhlExpress]: ["carrier_id", "test", "site_id", "password", "account_number"],
        [CarrierSettings.CarrierNameEnum.Eshipper]: ["carrier_id", "test", "username", "password"],
        [CarrierSettings.CarrierNameEnum.Freightcom]: ["carrier_id", "test", "username", "password"],
        [CarrierSettings.CarrierNameEnum.FedexExpress]: ["carrier_id", "test", "user_key", "password", "meter_number", "account_number"],
        [CarrierSettings.CarrierNameEnum.PurolatorCourier]: ["carrier_id", "test", "username", "password", "account_number", "user_token"],
        [CarrierSettings.CarrierNameEnum.UpsPackage]: ["carrier_id", "test", "username", "password", "access_license_number", "account_number"]
    }[carrier_name] || []).includes(property)
}

const FormInput: React.FC<any> = ({ label, ...props }) => {
    const Props = {
        type: "text",
        className: "input is-small",
        ...props
    };
    return (
        <div className="field">
            <label className="label">{label}</label>
            <div className="control">
                <input {...Props} />
            </div>
        </div>
    )
};

export default ConnectProviderModal;