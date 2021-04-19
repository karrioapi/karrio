import React, { useState, useRef, useContext } from 'react';
import { Shipment, ShipmentStatusEnum } from '@/api';
import LabelPrinter from './label/label-printer';
import { useNavigate } from '@reach/router';
import { NotificationType } from '@/library/types';
import ShipmentMutation from './data/shipment-mutation';
import { Notify } from './notifier';


interface ShipmentMenuComponent extends React.InputHTMLAttributes<HTMLDivElement> {
    shipment: Shipment;
}


const ShipmentMenu: React.FC<ShipmentMenuComponent> = ShipmentMutation<ShipmentMenuComponent>(({ shipment, voidLabel, ...props }) => {
    const { notify } = useContext(Notify);
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
    const createLabel = (_: React.MouseEvent) => {
        navigate('buy_label/' + shipment.id);
    };
    const cancelShipment = (shipment: Shipment) => async (e: React.MouseEvent) => {
        try {
            await voidLabel(shipment);
            notify({ type: NotificationType.success, message: 'Shipment successfully cancelled!' });
        } catch (err) {
            notify({ type: NotificationType.error, message: err });
        }
    };

    return (
        <div className={`dropdown is-right buttons has-addons ${isActive ? 'is-active' : ''}`} key={`menu-${shipment.id}`} {...props}>
            <div className="dropdown-trigger" style={{ width: '100%' }}>
                {shipment.status !== ShipmentStatusEnum.Created && <LabelPrinter shipment={shipment} style={{ width: '70%' }} />}
                {shipment.status === ShipmentStatusEnum.Created && <a className="button is-small" onClick={createLabel} style={{ width: '70%' }}>
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
});

export default ShipmentMenu;
