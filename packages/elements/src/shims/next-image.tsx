/**
 * Shim for next/legacy/image and next/image.
 * Renders a plain <img> tag in the embed context.
 */
import React from "react";

interface ImageProps extends React.ImgHTMLAttributes<HTMLImageElement> {
  src: string;
  width?: number | string;
  height?: number | string;
  alt?: string;
  layout?: string;
  objectFit?: string;
  priority?: boolean;
  placeholder?: string;
  blurDataURL?: string;
  loader?: any;
  unoptimized?: boolean;
}

function NextImage({ src, width, height, alt, layout, objectFit, priority, placeholder, blurDataURL, loader, unoptimized, ...rest }: ImageProps) {
  return (
    <img
      src={src}
      width={width}
      height={height}
      alt={alt || ""}
      {...rest}
    />
  );
}

export default NextImage;
