"use client";
import { useAppMode } from "@karrio/hooks/app-mode";
import Link, { LinkProps } from "next/link";
import { p } from "@karrio/lib";
import React from "react";
import { SidebarContext } from "@karrio/ui/components/ui/sidebar";

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
  // Optionally use sidebar context - don't throw error if not available
  const sidebarContext = React.useContext(SidebarContext);

  const handleClick = (e: React.MouseEvent<HTMLAnchorElement, MouseEvent>) => {
    // Close mobile sidebar on navigation if sidebar context is available
    if (sidebarContext) {
      sidebarContext.setOpenMobile(false);
    }

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
