import { state } from '@/library/api';
import { Shipment } from '@purplship/purplship';
import React, { useState } from 'react';

interface LabelPrinterComponent {
    shipment: Shipment;
}

const LabelPrinter: React.FC<LabelPrinterComponent> = ({ shipment }) => {
    const [isActive, setIsActive] = useState<boolean>(false);
    const close = (evt?: React.MouseEvent) => {
        evt?.preventDefault();
        setIsActive(false);
    }
    const source = "data:application/pdf;base64," + encodeURI(shipment.label as string);

    return (
        <>
            <button className="button is-small" onClick={() => setIsActive(true)}>
                <span>Print Label</span>
            </button>

            <div className={`modal ${isActive ? "is-active" : ""}`}>
                <div className="modal-background" onClick={close}></div>
                <div className="label-container">

                    <iframe src={source} height="100%" width="100%"></iframe>

                </div>
                <button className="modal-close is-large" aria-label="close" onClick={close}></button>
            </div>
        </>
    )
};

export default LabelPrinter;