import { useAppMode } from '@/context/app-mode';
import Link, { LinkProps } from 'next/link';
import { p } from '@/lib/client';
import React from 'react';

interface AppLinkProps extends LinkProps {
  href: string;
  target?: string;
  className?: string;
  onClick?: (e: React.MouseEvent<HTMLAnchorElement, MouseEvent>) => void;
}

const AppLink: React.FC<AppLinkProps> = ({ href, className, target, onClick, children, ...props }) => {
  const { basePath } = useAppMode();

  return (
    <Link href={p`${basePath}${href}`} {...props} legacyBehavior>
      <a
        {...(target ? { target } : {})}
        {...(onClick ? { onClick } : {})}
        {...(className ? { className } : {})}>
        {children}
      </a>
    </Link>
  )
};

export default AppLink;
