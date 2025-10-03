"use client";
import { useAppMode } from "@karrio/hooks/app-mode";
import Link, { LinkProps } from "next/link";
import { p } from "@karrio/lib";
import React from "react";
import { useSidebar } from "@karrio/ui/components/ui/sidebar";

interface AppLinkProps extends LinkProps<HTMLElement> {
  href: string;
  target?: string;
  className?: string;
  onClick?: (e: React.MouseEvent<HTMLAnchorElement, MouseEvent>) => void;
  children?: React.ReactNode;
  style?: React.CSSProperties;
}

export const AppLink = ({
  href,
  className,
  target,
  onClick,
  children,
  style,
  ...props
}: AppLinkProps): JSX.Element => {
  const { basePath } = useAppMode();
  const { setOpenMobile } = useSidebar();

  const handleClick = (e: React.MouseEvent<HTMLAnchorElement, MouseEvent>) => {
    // Close mobile sidebar on navigation
    setOpenMobile(false);

    // Call the original onClick if provided
    onClick?.(e);
  };

  return (
    <Link href={p`${basePath}${href}`} {...props} legacyBehavior>
      <a
        {...(style ? { style } : {})}
        {...(target ? { target } : {})}
        onClick={handleClick}
        {...(className ? { className } : {})}
      >
        {children}
      </a>
    </Link>
  );
};
