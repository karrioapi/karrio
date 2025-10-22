import { CARRIER_IMAGES, CarrierNameEnum, IMAGES } from "@karrio/types";
import { isNoneOrEmpty, p, formatCarrierSlug, getInitials, snakeCase } from "@karrio/lib";
import Image from "next/legacy/image";
import React from "react";

interface CarrierImageComponent
  extends React.AllHTMLAttributes<HTMLImageElement> {
  carrier_name?: CarrierNameEnum | string;
  containerClassName?: string;
  text_color?: string;
  background?: string;
}

export const CarrierImage = ({
  carrier_name,
  text_color,
  background,
  containerClassName,
  className,
  width,
  height,
  ...props
}: CarrierImageComponent): JSX.Element => {
  const carrierName = snakeCase(carrier_name);
  const carrier_img = CARRIER_IMAGES[carrierName as any] || carrierName;
  const has_image = IMAGES.includes(carrierName as string);
  const has_styling = !isNoneOrEmpty(text_color) || !isNoneOrEmpty(background);

  const _name = carrierName;
  const isIcon = true;  // We always use icon format for this component
  const carrier_label = (isIcon
    ? getInitials(_name).substring(0, 2)
    : formatCarrierSlug(_name)
  );
  const svg_text_color = isNoneOrEmpty(text_color) ? "#ddd" : text_color;
  const svg_background = isNoneOrEmpty(background) ? "#7e51e1" : background;
  const props_str = 'viewBox="0 0 512 512"';
  const path = `<path xmlns="http://www.w3.org/2000/svg" style="fill-rule:evenodd;clip-rule:evenodd;fill:${svg_background};" d="M512,472c0,22.1-17.9,40-40,40H40c-22.1,0-40-17.9-40-40V40C0,17.9,17.9,0,40,0h432c22.1,0,40,17.9,40,40V472z"/>`;

  const svg_content = `<svg ${props_str} x="0px" y="0px" xmlns="http://www.w3.org/2000/svg">
    <g>
      ${path}
      <text x="50%" y="55%" alignment-baseline="middle" text-anchor="middle" fill="${svg_text_color}" font-weight="bold" font-family="arial"
        font-size="16em" style="text-transform: uppercase; border-radius: 40px;">
        ${carrier_label}
      </text>
    </g>
  </svg>`;

  return (
    <div className={containerClassName || "m-1"} {...props}>
      {has_image && !has_styling ? (
        <Image
          src={p`/carriers/${carrier_img as string}_icon.svg`}
          width={(width as number) || 60}
          height={(height as number) || 60}
          alt={carrier_name}
          className={className || ""}
        />
      ) : (
        <img
          src={`data:image/svg+xml;charset=utf-8,${encodeURIComponent(svg_content)}`}
          width={(width as number) || 60}
          height={(height as number) || 60}
          alt={carrier_name}
          className={className || ""}
        />
      )}
    </div>
  );
};
