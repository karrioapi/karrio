import { Shipment } from '@purplship/purplship';
import React, { useState } from 'react';

interface LabelPrinterComponent extends React.ButtonHTMLAttributes<HTMLButtonElement> {
    shipment: Shipment;
}

const LabelPrinter: React.FC<LabelPrinterComponent> = ({ shipment, ...props }) => {
    const [isActive, setIsActive] = useState<boolean>(false);
    const close = (evt?: React.MouseEvent) => {
        evt?.preventDefault();
        setIsActive(false);
    }
    const label_type = shipment?.label_type || Shipment.LabelTypeEnum.PDF;
    const format = {
        [Shipment.LabelTypeEnum.PDF]: 'application/pdf',
        [Shipment.LabelTypeEnum.ZPL]: 'application/zpl'
    }[label_type];
    const source = `data:${format};base64, ${encodeURI(shipment.label as string)}`;

    return (
        <>
            <button className="button is-small" onClick={() => setIsActive(true)} {...props}>
                <span>Print Label</span>
            </button>

            <div className={`modal ${isActive ? "is-active" : ""}`}>
                <div className="modal-background" onClick={close}></div>
                <div className="label-container">

                    {isActive && <iframe src={source} height="100%" width="100%"></iframe>}

                </div>
                <button className="modal-close is-large" aria-label="close" onClick={close}></button>
            </div>
        </>
    )
};

export default LabelPrinter;