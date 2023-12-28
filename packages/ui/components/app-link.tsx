import { useAppMode } from '@karrio/hooks/app-mode';
import Link, { LinkProps } from 'next/link';
import { p } from '@karrio/lib';
import React from 'react';

interface AppLinkProps extends LinkProps<HTMLElement> {
  href: string;
  target?: string;
  className?: string;
  onClick?: (e: React.MouseEvent<HTMLAnchorElement, MouseEvent>) => void;
  children?: React.ReactNode;
  style?: React.CSSProperties;
}

export const AppLink: React.FC<AppLinkProps> = ({ href, className, target, onClick, children, style, ...props }) => {
  const { basePath } = useAppMode();

  return (
    <Link href={p`${basePath}${href}`} {...props} legacyBehavior>
      <a
        {...(style ? { style } : {})}
        {...(target ? { target } : {})}
        {...(onClick ? { onClick } : {})}
        {...(className ? { className } : {})}>
        {children}
      </a>
    </Link>
  )
};
