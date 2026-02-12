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

/**
 * Rewrites absolute /carriers/ paths to relative ./carriers/ so the iframe
 * resolves them against its own origin (where the SVGs are co-located).
 */
function resolveSrc(src: string): string {
  if (src.startsWith("/carriers/")) {
    return "." + src;
  }
  return src;
}

function NextImage({ src, width, height, alt, layout, objectFit, priority, placeholder, blurDataURL, loader, unoptimized, ...rest }: ImageProps) {
  return (
    <img
      src={resolveSrc(src)}
      width={width}
      height={height}
      alt={alt || ""}
      {...rest}
    />
  );
}

export default NextImage;
