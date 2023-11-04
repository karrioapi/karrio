import { formatCustomsLabel, formatRef, isNone, isNoneOrEmpty } from '@/lib/helper';
import { CustomsType } from '@/lib/types';
import React from 'react';

interface CustomsInfoDescriptionComponent {
  customs: CustomsType;
}

const CustomsInfoDescription: React.FC<CustomsInfoDescriptionComponent> = ({ customs }) => {
  return (
    <>

      <p className="is-size-7 my-1 has-text-weight-semibold">{formatCustomsLabel(customs)}</p>

      {Object.entries(customs.options || {}).map(([key, value]: any, index) => <React.Fragment key={index + "option-info"}>
        {!isNoneOrEmpty(value) && <p className="is-subtitle is-size-7 my-1 has-text-weight-semibold has-text-grey">
          <span>
            {formatRef(key).toLowerCase()}: <strong>{String(value)}</strong>
          </span>
        </p>}
      </React.Fragment>)}

      <p className="is-size-7 my-1 has-text-weight-semibold has-text-grey">
        {isNone(customs?.invoice) ? '' : <span>Invoice Number: <strong>{customs.invoice}</strong></span>}
      </p>
      <p className="is-size-7 my-1 has-text-weight-semibold has-text-grey">
        {isNone(customs?.invoice_date) ? '' : <span>Invoice Date: <strong>{customs.invoice_date}</strong></span>}
      </p>
      <p className="is-size-7 my-1 has-text-weight-semibold has-text-grey">
        {!customs?.signer ? '' : <span>{customs?.certify && `Certified and `}Signed By <strong>{customs.signer}</strong></span>}
      </p>
      <p className="is-size-7 my-1 has-text-weight-semibold has-text-grey">
        {isNone(customs?.content_description) ? '' : <span><strong>Content:</strong> {customs.content_description}</span>}
      </p>

      {/* Options section */}
      {(Object.values(customs.duty as object).length > 0) && <div className="is-6 is-size-6 py-1">

        <p className="is-title is-size-7 my-2 has-text-weight-semibold">DUTIES</p>

        {Object.entries(customs.duty || {}).map(([key, value]: any, index) => <React.Fragment key={index + "option-info"}>
          {!isNoneOrEmpty(value) && <p className="is-subtitle is-size-7 my-1 has-text-weight-semibold has-text-grey">
            <span>
              {formatRef(key).toLowerCase()}: <strong>{formatRef(String(value))}</strong>
            </span>
          </p>}
        </React.Fragment>)}
      </div>}

    </>
  );
};

export default CustomsInfoDescription;
