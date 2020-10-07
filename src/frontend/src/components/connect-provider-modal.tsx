import { Provider, state } from '@/library/api';
import { CarrierSettings } from '@purplship/purplship/dist';
import React, { useState } from 'react';
import { Reference } from '@/library/context';

interface ConnectProviderModalComponent {
    provider?: Provider;
    className?: string;
}

const ConnectProviderModal: React.FC<ConnectProviderModalComponent> = ({ children, provider, className }) => {
    const [isNew, _] = useState<boolean>(provider === null || provider === undefined);
    const [payload, setPayload] = useState<Partial<Provider>>(provider || { carrierName: undefined });
    const [error, setError] = useState<string>("");
    const [isActive, setIsActive] = useState<boolean>(false);
    const [isDisabled, setIsDisabled] = useState<boolean>(false);
    const [hasError, setHasError] = useState<boolean>(false);

    const handleSubmit = async (evt: React.FormEvent<HTMLFormElement>) => {
        evt.preventDefault();
        try {
            setIsDisabled(true);
            const data = {
                carrier_name: payload.carrierName as CarrierSettings.CarrierNameEnum,
                carrier_config: payload
            };
            if (isNew) {
                await state.connectProvider(data);
            } else {
                await state.updateProvider(payload.id as string, data);
            }
            close();
        } catch (err) {
            setHasError(true);
            setError(err.message);
            setIsDisabled(false);
        }
    };
    const close = (evt?: React.MouseEvent) => {
        evt?.preventDefault();
        setHasError(false);
        setIsDisabled(false);
        setIsActive(false);
    }
    const handleOnChange = (property: string) => (e: React.ChangeEvent<any>) => {
        e.preventDefault();
        setPayload({ ...payload, [property]: e.target.value || undefined });
    };
    const has = (property: string) => {
        return hasProperty(payload.carrierName as CarrierSettings.CarrierNameEnum, property);
    };

    return (
        <>
            <button className={className} onClick={() => setIsActive(true)}>
                {children}
            </button>

            <div className={`modal ${isActive ? "is-active" : ""}`}>
                <div className="modal-background" onClick={close}></div>
                <form className="modal-card" onSubmit={handleSubmit}>
                    <section className="modal-card-body">
                        <h3 className="subtitle is-3">Connect a Carrier</h3>
                        <p className="is-size-7 has-text-danger my-1" style={{ visibility: (hasError ? "visible" : "hidden") }}>{error}</p>

                        <div className="field">
                            <div className="select is-fullwidth">
                                <select defaultValue={payload.carrierName} onChange={handleOnChange("carrierName")} disabled={!isNew} required>
                                    <option value=''>Select Carrier</option>

                                    <Reference.Consumer>
                                        {(ref) => (Object.values(ref || {}).length > 0) && Object.keys(ref.carriers).map(carrier => (
                                            <option key={carrier} value={carrier}>{ref.carriers[carrier]}</option>
                                        ))}
                                    </Reference.Consumer>

                                </select>
                            </div>
                        </div>

                        {(payload.carrierName !== undefined) &&
                            <>
                                <hr />

                                <FormInput label="Carrier Id" defaultValue={payload.carrierId} onChange={handleOnChange("carrierId")} required/>

                                {/* Carrier specific fields BEGING */}

                                {has("siteId") && <FormInput label="Site Id" defaultValue={payload.siteId} onChange={handleOnChange("siteId")} required/>}

                                {has("username") && <FormInput label="Username" defaultValue={payload.username} onChange={handleOnChange("username")} required/>}

                                {has("password") && <FormInput label="Password" defaultValue={payload.password} onChange={handleOnChange("password")} required/>}

                                {has("customerNumber") && <FormInput label="Customer Number" defaultValue={payload.customerNumber} onChange={handleOnChange("customerNumber")} required/>}

                                {has("contractId") && <FormInput label="Contract Id" defaultValue={payload.contractId} onChange={handleOnChange("contractId")} />}

                                {has("accountNumber") && <FormInput label="Account Number" defaultValue={payload.accountNumber} onChange={handleOnChange("accountNumber")} required/>}

                                {has("userKey") && <FormInput label="User Key" defaultValue={payload.userKey} onChange={handleOnChange("userKey")} />}

                                {has("meterNumber") && <FormInput label="Meter Number" defaultValue={payload.meterNumber} onChange={handleOnChange("meterNumber")} required/>}

                                {has("userToken") && <FormInput label="User Token" defaultValue={payload.userToken} onChange={handleOnChange("userToken")} />}

                                {has("accessLicenseNumber") && <FormInput label="Access License Number" defaultValue={payload.accessLicenseNumber} onChange={handleOnChange("accessLicenseNumber")} required/>}

                                {/* Carrier specific fields END */}

                                <div className="field">
                                    <div className="control">
                                        <label className="checkbox">
                                            <input type="checkbox" defaultChecked={payload.test} onChange={handleOnChange("test")}/> Test Mode
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

function hasProperty(carrierName: CarrierSettings.CarrierNameEnum, property: string): boolean {
    // TODO: Use carriers settings types when available for automatic validation
    return ({
        [CarrierSettings.CarrierNameEnum.Canadapost]: ["username", "password", "customerNumber", "contractId"],
        [CarrierSettings.CarrierNameEnum.DhlExpress]: ["siteId", "password", "accountNumber"],
        [CarrierSettings.CarrierNameEnum.Eshipper]: ["username", "password"],
        [CarrierSettings.CarrierNameEnum.Freightcom]: ["username", "password"],
        [CarrierSettings.CarrierNameEnum.FedexExpress]: ["userKey", "password", "meterNumber", "accountNumber"],
        [CarrierSettings.CarrierNameEnum.PurolatorCourier]: ["username", "password", "accountNumber", "userToken"],
        [CarrierSettings.CarrierNameEnum.UpsPackage]: ["username", "password", "accessLicenseNumber", "accountNumber"]
    }[carrierName] || []).includes(property)
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