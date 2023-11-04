import { formatRef, isNone } from '@/lib/helper';
import { RateType } from '@/lib/types';
import React from 'react';

interface RateDescriptionComponent {
  rate: RateType;
}

const RateDescription: React.FC<RateDescriptionComponent> = ({ rate }) => {
  return (
    <div className="column px-2 py-0 is-size-7 has-text-weight-semibold">
      <h6 className="has-text-weight-bold text-ellipsis" style={{ maxWidth: '100%' }}>
        {formatRef(((rate.meta as any)?.service_name || rate.service) as string)}
      </h6>
      <p className="has-text-grey m-0 p-0 text-ellipsis" style={{ maxWidth: '100%' }}>
        <span>{rate.total_charge} {rate.currency}</span>
        {!isNone(rate.transit_days) && <span> - {rate.transit_days} Transit days</span>}
      </p>
      <p className="has-text-info mt-1 p-0 text-ellipsis" style={{ fontSize: '0.8rem', maxWidth: '100%' }}>
        <span>{rate.carrier_name}:{rate.carrier_id}</span>
      </p>
    </div>
  );
};

export default RateDescription;
