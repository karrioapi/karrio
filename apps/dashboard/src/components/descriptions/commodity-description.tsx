import { formatWeight, isNoneOrEmpty } from '@/lib/helper';
import { CommodityType } from '@/lib/types';
import React from 'react';

interface CommodityDescriptionComponent extends React.HTMLAttributes<any> {
  commodity: CommodityType;
  prefix?: string;
  suffix?: string;
  comments?: string;
}

const CommodityDescription: React.FC<CommodityDescriptionComponent> = ({ commodity, prefix, suffix, comments, className }) => {
  return (
    <div className={`is-flex ${className || ''}`}>
      <div className="is-flex-grow-3 p-0 text-ellipsis">
        <p className="is-size-7 my-1 has-text-weight-semibold">
          {prefix} {`${commodity.title || commodity.description || 'Item'}`} {suffix}
        </p>
        <p className="is-size-7 my-1 has-text-weight-semibold has-text-grey">
          {isNoneOrEmpty(commodity.sku) ? ' SKU: 0000000' : ` SKU: ${commodity.sku}`}
          {isNoneOrEmpty(commodity.hs_code) ? '' : ` | HS code: ${commodity.hs_code}`}
        </p>
      </div>

      <div className="is-flex-grow-1 p-0 has-text-right" style={{ minWidth: '90px' }}>
        <p className="is-size-7 my-1 has-text-weight-semibold">
          {commodity.quantity}{' x '}{formatWeight(commodity)}
        </p>
        <p className="is-size-7 my-1 has-text-weight-semibold has-text-info">
          {comments}
        </p>
      </div>
    </div>
  );
};

export default CommodityDescription;
