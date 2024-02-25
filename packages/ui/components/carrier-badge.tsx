import { CARRIER_IMAGES, CarrierSettingsCarrierNameEnum } from '@karrio/types';
import { isNoneOrEmpty, p } from '@karrio/lib';
import Image from "next/image";
import React from 'react';


interface CarrierBadgeComponent extends React.AllHTMLAttributes<HTMLDivElement> {
  carrier_name?: CarrierSettingsCarrierNameEnum | string;
  width?: number;
  height?: number;
  text_color?: string;
  background?: string;
}

export const CarrierBadge: React.FC<CarrierBadgeComponent> = ({ carrier_name, text_color, background, className, width, height, ...props }) => {
  const carrier_img = CARRIER_IMAGES[carrier_name as any] || carrier_name;
  const query = new URLSearchParams(JSON.parse(JSON.stringify({
    text_color: !!text_color ? encodeURIComponent(text_color) : undefined,
    background: !!background ? encodeURIComponent(background) : undefined,
  }))).toString();

  return (
    <div className='mt-1'>
      {isNoneOrEmpty(query) ?
        <Image
          src={p`/carriers/${carrier_img}_logo.svg`}
          alt={carrier_name || "logo"}
          height={height || 14}
          width={width || 70}
        /> :
        <img
          src={p`/carriers/${carrier_img}_logo.svg?${query}`}
          alt={carrier_name || "logo"}
          height={height || 14}
          width={width || 70}
        />
      }
    </div>
  );
};
