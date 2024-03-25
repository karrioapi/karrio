import { CARRIER_IMAGES, CarrierSettingsCarrierNameEnum } from '@karrio/types';
import { isNoneOrEmpty, p } from '@karrio/lib';
import Image from "next/legacy/image";
import React from 'react';


interface CarrierImageComponent extends React.AllHTMLAttributes<HTMLImageElement> {
  carrier_name?: CarrierSettingsCarrierNameEnum | string;
  containerClassName?: string;
  text_color?: string;
  background?: string;
}

export const CarrierImage: React.FC<CarrierImageComponent> = ({ carrier_name, text_color, background, containerClassName, className, width, height, ...props }) => {
  const carrier_img = CARRIER_IMAGES[carrier_name as any] || carrier_name;
  const query = new URLSearchParams(JSON.parse(JSON.stringify({
    text_color: !!text_color ? encodeURIComponent(text_color) : undefined,
    background: !!background ? encodeURIComponent(background) : undefined,
  }))).toString();

  return (
    <div className={containerClassName || 'm-1'} {...props}>
      {isNoneOrEmpty(query) ?
        <Image
          src={p`/carriers/${carrier_img as string}_icon.svg`}
          width={width as number || 60} height={height as number || 60}
          alt={carrier_name}
          className={className || ''}
        /> :
        <img
          src={p`/carriers/${carrier_img as string}_icon.svg?${query}`}
          width={width as number || 60} height={height as number || 60}
          alt={carrier_name}
          className={className || ''}
        />
      }
    </div>
  );
};
