import { formatRef, isNone } from '@karrio/lib';
import { RateType } from '@karrio/types';
import React from 'react';

interface RateDescriptionComponent {
  rate: RateType;
}

export const RateDescription: React.FC<RateDescriptionComponent> = ({ rate }) => {
  return (
    <div className="column px-2 py-1 is-size-7 has-text-weight-semibold text-ellipsis" style={{ maxWidth: '190px', lineHeight: '13px' }}>
      <span className="has-text-weight-bold text-ellipsis m-0" style={{ maxWidth: '100%' }}>
        {formatRef(((rate.meta as any)?.service_name || rate.service) as string)}
      </span><br />
      <span className="has-text-grey m-0 p-0 text-ellipsis" style={{ maxWidth: '100%' }}>
        <span>{rate.total_charge} {rate.currency}</span>
        {!isNone(rate.transit_days) && <span> - {rate.transit_days} Transit days</span>}
      </span><br />
      <span className="has-text-info m-0 p-0 text-ellipsis" style={{ fontSize: '0.75rem', maxWidth: '100%' }}>
        {rate.carrier_name}:{rate.carrier_id}
      </span>
    </div>
  );
};
