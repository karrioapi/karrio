import React, { useState, useRef } from 'react';
import { Shipment, ShipmentStatusEnum } from '@/api';
import LabelPrinter from './label/label-printer';
import { useNavigate } from '@reach/router';
import { state } from '@/library/app';
import { NotificationType } from '@/library/types';


interface ShipmentMenuComponent extends React.AllHTMLAttributes<HTMLDivElement> {
    shipment: Shipment;
}


const ShipmentMenu: React.FC<ShipmentMenuComponent> = ({ shipment, ...props }) => {
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
        navigate('buy_label/' + shipment.id);
        state.setLabelData({ shipment });
    };
    const cancelShipment = (shipment: Shipment) => async (e: React.MouseEvent) => {
        try {
            await state.voidLabel(shipment);
            state.setNotification({ type: NotificationType.success, message: 'Shipment successfully cancelled!' });
        } catch (err) {
            state.setNotification({ type: NotificationType.error, message: err });
        }
    };

    return (
        <div className={`dropdown is-right buttons has-addons ${isActive ? 'is-active' : ''}`} key={`menu-${shipment.id}`} {...props}>
            <div className="dropdown-trigger" style={{width: '100%'}}>
                {shipment.status !== ShipmentStatusEnum.Created && <LabelPrinter shipment={shipment} style={{width: '70%'}} />}
                {shipment.status === ShipmentStatusEnum.Created && <a className="button is-small" onClick={createLabel} style={{width: '70%'}}>
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
