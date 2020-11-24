import React, { useState, useRef } from 'react';
import { ErrorResponse, Shipment } from '@purplship/purplship';
import LabelPrinter from './label/label-printer';
import { useNavigate } from '@reach/router';
import { NotificationType, state } from '@/library/api';


interface ShipmentMenuComponent {
    shipment: Shipment;
}


const ShipmentMenu: React.FC<ShipmentMenuComponent> = ({ shipment }) => {
    const [isActive, setIsActive] = useState(false);
    const btn = useRef<HTMLButtonElement>(null);
    const navigate = useNavigate();
    const handleOnClick = (e: React.MouseEvent) => {
        if (!isActive) {
            setIsActive(true);
            document.addEventListener('click', onBodyClick);
        }
        e.stopPropagation();
    };
    const onBodyClick = (e: MouseEvent) => {
        if (e.target !== btn.current) {
            setIsActive(false);
            document.removeEventListener('click', onBodyClick);
        }
    };
    const createLabel = (e: React.MouseEvent) => {
        navigate('create/label');
        state.setLabelData({ shipment });
    };
    const cancelShipment = (shipment: Shipment) => (e: React.MouseEvent) => {
        try {
            state.cancelShipment(shipment);
            state.setNotification({ type: NotificationType.success, message: 'Shipment successfully cancelled!' });
        } catch (err) {
            let message = err.message
            if (err.response?.error !== undefined) {
                message = ((err.response.error.details as ErrorResponse).messages || []).map(msg => (
                    <p>{msg.carrier_name}: {msg.message}</p>
                ))
            }
            state.setNotification({ type: NotificationType.error, message });
        }
    };

    return (
        <div className={`dropdown is-right buttons has-addons ${isActive ? 'is-active' : ''}`} key={`menu-${shipment.id}`} >
            <div className="dropdown-trigger">
                {shipment.status !== Shipment.StatusEnum.Created && <LabelPrinter shipment={shipment} />}
                {shipment.status === Shipment.StatusEnum.Created && <a className="button is-small" onClick={createLabel}>
                    <span>Buy Label</span>
                </a>}
                <button
                    id={shipment.id}
                    className="button is-small"
                    aria-haspopup="true"
                    aria-controls={`shipment-menu-${shipment.id}`}
                    onClick={handleOnClick}
                    ref={btn}>
                    <span className="icon is-small">
                        <i className="fas fa-angle-down" aria-hidden="true"></i>
                    </span>
                </button>
            </div>

            <div className="dropdown-menu" id={`shipment-menu-${shipment.id}`} role="menu">
                <div className="dropdown-content">
                    <a href="#" className="dropdown-item" onClick={cancelShipment(shipment)}>Cancel Shipment</a>
                </div>
            </div>
        </div>
    );
}

export default ShipmentMenu;
