import React, { useContext, useEffect, useState } from 'react';
import InputField from '@/components/generic/input-field';
import { NotificationType } from '@/library/types';
import ButtonField from '@/components/generic/button-field';
import SelectField from '@/components/generic/select-field';
import { APIReference } from '@/components/data/references-query';
import { UserConnections, UserConnectionType } from '@/components/data/user-connections-query';
import { SystemConnections, SystemConnectionType } from '@/components/data/system-connections-query';
import TrackerMutation from '@/components/data/tracker-mutation';
import { Notify } from './notifier';

type Connection = UserConnectionType | SystemConnectionType;
interface TrackShipmentModalComponent {
    className?: string;
    onUpdate?: () => void;
}

const TrackShipmentModal: React.FC<TrackShipmentModalComponent> = TrackerMutation<TrackShipmentModalComponent>(
    ({ children, className, onUpdate, createTracker }) => {
        const { notify } = useContext(Notify);
        const { carriers } = useContext(APIReference);
        const { user_connections, ...user } = useContext(UserConnections);
        const { system_connections, ...system } = useContext(SystemConnections);
        const [isActive, setIsActive] = useState<boolean>(false);
        const [key, setKey] = useState<string>(`tracker-${Date.now()}`);
        const [carrier, setCarrier] = useState<Connection>();
        const [trackingNumber, setTrackingNumber] = useState<string>();
        
        const close = (_?: React.MouseEvent) => {
            setCarrier(undefined);
            setTrackingNumber(undefined);
            setKey(`tracker-${Date.now()}`);
            setIsActive(false);
            onUpdate && onUpdate();
        };
        const create = async (evt: React.FormEvent<HTMLFormElement>) => {
            evt.preventDefault();
            try {
                await createTracker(trackingNumber as string, carrier?.carrier_name as string, carrier?.test as boolean);
                notify({ type: NotificationType.success, message: 'Tracker successfully added!' });
                close();
            } catch (message) {
                notify({ type: NotificationType.error, message });
            }
        };
        const updateCarrier = (carrierId: string) => {
            const all_carriers = [...(user_connections || []), ...(system_connections || [])];
            const carrier = all_carriers.find(carrier => carrier?.carrier_id === carrierId);
            setCarrier(carrier);
        };

        useEffect(() => { if (!user.loading) user.load(); }, []);
        useEffect(() => { if (!system.loading) system.load(); }, []);

        return (
            <>
                <button className={className} onClick={() => setIsActive(true)}>
                    {children}
                </button>

                <div className={`modal ${isActive ? "is-active" : ""}`} key={key}>
                    <div className="modal-background" onClick={close}></div>
                    <form className="modal-card" onSubmit={create}>
                        <section className="modal-card-body">
                            <h3 className="subtitle is-3">Track a Shipment</h3>

                            <InputField label="Tracking Number" defaultValue={trackingNumber} onChange={e => setTrackingNumber(e.target.value)} fieldClass="mt-6" required />

                            <SelectField label="Carrier" onChange={e => updateCarrier(e.target.value)} className="is-fullwidth" required>
                                <option value="">Select a carrier</option>

                                {[...(user_connections || []), ...(system_connections || [])].map((carrier, index) => (
                                    <option key={index} value={carrier.carrier_id}>
                                        {`${(carriers as any)[carrier.carrier_name]} ${carrier.test ? '(Sandbox)' : ''}`}
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
    });

export default TrackShipmentModal;