import React, { useContext, useEffect, useState } from 'react';
import InputField from '@/components/generic/input-field';
import { Reference, SystemConnections, UserConnections } from '@/library/context';
import { state } from '@/library/app';
import { Connection, NotificationType } from '@/library/types';
import ButtonField from './generic/button-field';
import SelectField from './generic/select-field';

interface TrackShipmentModalComponent {
    className?: string;
}

const TrackShipmentModal: React.FC<TrackShipmentModalComponent> = ({ children, className }) => {
    const Ref = useContext(Reference);
    const userConnections = useContext(UserConnections);
    const systemConnections = useContext(SystemConnections);
    const [isActive, setIsActive] = useState<boolean>(false);
    const [isLoading, setIsLoading] = useState<boolean>(false);
    const [key, setKey] = useState<string>(`tracker-${Date.now()}`);
    const [carrier, setCarrier] = useState<Connection>();
    const [trackingNumber, setTrackingNumber] = useState<string>();
    const close = (_?: React.MouseEvent) => {
        setCarrier(undefined);
        setTrackingNumber(undefined);
        setKey(`tracker-${Date.now()}`);
        setIsActive(false);
    };
    const createTracker = async (evt: React.FormEvent<HTMLFormElement>) => {
        evt.preventDefault();
        try {
            await state.createTracker(carrier as Connection, trackingNumber as string)
            close();
        } catch (message) {
            state.setNotification({ type: NotificationType.error, message });
        }
    };
    const updateCarrier = (carrierId: string) => {
        const all_carriers = [...(userConnections?.results || []), ...(systemConnections?.results || [])];
        const carrier = all_carriers.find(carrier => carrier.carrier_id === carrierId);
        setCarrier(carrier);
    };
    useEffect(() => {
        if (isLoading) return;
        if (userConnections === undefined || userConnections.fetched === false) {
            setIsLoading(true);
            state.fetchUserConnections().catch(_ => _).then(() => setIsLoading(false));
        }
        if (systemConnections === undefined || systemConnections.fetched === false) {
            setIsLoading(true);
            state.fetchSystemConnections().catch(_ => _).then(() => setIsLoading(false));
        }
    }, [systemConnections, userConnections, Ref?.carriers]);

    return (
        <>
            <button className={className} onClick={() => setIsActive(true)}>
                {children}
            </button>

            <div className={`modal ${isActive ? "is-active" : ""}`} key={key}>
                <div className="modal-background" onClick={close}></div>
                <form className="modal-card" onSubmit={createTracker}>
                    <section className="modal-card-body">
                        <h3 className="subtitle is-3">Track a Shipment</h3>

                        <InputField label="Tracking Number" defaultValue={trackingNumber} onChange={e => setTrackingNumber(e.target.value)} fieldClass="mt-6" required />

                        <SelectField label="Carrier" onChange={e => updateCarrier(e.target.value)} className="is-fullwidth" required>
                            <option value="">Select a carrier</option>

                            {[...(userConnections?.results || []), ...(systemConnections?.results || [])].map((carrier, index) => (
                                <option key={index} value={carrier.carrier_id}>
                                    {`${(Ref?.carriers as any)[carrier.carrier_name.toString()]} ${carrier.test ? '(Sandbox)' : ''}`}
                                </option>
                            ))}
                        </SelectField>

                        <ButtonField type="submit" className="is-primary" fieldClass="has-text-centered mt-6">
                            <span>Submit</span>
                        </ButtonField>
                    </section>
                </form>
                <button className="modal-close is-large" aria-label="close" onClick={close}></button>
            </div>
        </>
    )
};

export default TrackShipmentModal;