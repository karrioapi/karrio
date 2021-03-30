import React from 'react';
import { Customs } from '@/api';
import { formatCustomsLabel, formatRef, isNone } from '@/library/helper';

interface CustomsInfoDescriptionComponent {
    customs: Customs;
}

const CustomsInfoDescription: React.FC<CustomsInfoDescriptionComponent> = ({ customs }) => {
    return (
        <>

            <p className="is-subtitle is-size-7 my-1 has-text-weight-semibold">{formatCustomsLabel(customs)}</p>
            <p className="is-subtitle is-size-7 my-1 has-text-weight-semibold has-text-grey">
                {isNone(customs?.aes) ? '' : <span>AES: <strong>{customs.aes}</strong></span>}
            </p>
            <p className="is-subtitle is-size-7 my-1 has-text-weight-semibold has-text-grey">
                {isNone(customs?.eel_pfc) ? '' : <span>EEL / PFC: <strong>{customs.eel_pfc}</strong></span>}
            </p>
            <p className="is-subtitle is-size-7 my-1 has-text-weight-semibold has-text-grey">
                {isNone(customs?.invoice) ? '' : <span>Invoice Number: <strong>{customs.invoice}</strong></span>}
            </p>
            <p className="is-subtitle is-size-7 my-1 has-text-weight-semibold has-text-grey">
                {isNone(customs?.certificate_number) ? '' : <span>Certificate Number: <strong>{customs.certificate_number}</strong></span>}
            </p>
            <p className="is-subtitle is-size-7 my-1 has-text-weight-semibold has-text-grey">
                {isNone(customs.duty) ? '' : <span>Duties paid by <strong>{formatRef('' + customs.duty?.paid_by)}</strong></span>}
            </p>
            <p className="is-subtitle is-size-7 my-1 has-text-weight-semibold has-text-grey">
                {!customs?.certify ? '' : <span>Certified and Signed By <strong>{customs.signer}</strong></span>}
            </p>
            <p className="is-subtitle is-size-7 my-1 has-text-weight-semibold has-text-grey">
                {isNone(customs?.content_description) ? '' : <span><strong>Content:</strong> {customs.content_description}</span>}
            </p>

        </>
    );
};

export default CustomsInfoDescription;
