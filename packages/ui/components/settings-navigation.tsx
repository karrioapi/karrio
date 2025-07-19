"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { cn } from "@karrio/ui/lib/utils";
import { useAPIMetadata } from "@karrio/hooks/api-metadata";

interface SettingsNavigationProps {
  showOrganization?: boolean;
}

const settingsItems = [
  {
    key: "account",
    label: "Account",
    href: "/settings/account",
  },
  {
    key: "profile",
    label: "Profile",
    href: "/settings/profile",
  },
  {
    key: "organization",
    label: "Organization",
    href: "/settings/organization",
    requiresOrg: true,
  },
  {
    key: "addresses",
    label: "Addresses",
    href: "/settings/addresses",
  },
  {
    key: "parcels",
    label: "Parcels",
    href: "/settings/parcels",
  },
  {
    key: "templates",
    label: "Templates",
    href: "/settings/templates",
  },
];

export function SettingsNavigation({ showOrganization }: SettingsNavigationProps) {
  const pathname = usePathname();
  const { references } = useAPIMetadata();

  // Auto-detect multi-organization support
  const isMultiOrg = references?.MULTI_ORGANIZATIONS || showOrganization;

  const filteredItems = settingsItems.filter(item =>
    !item.requiresOrg || isMultiOrg
  );

  return (
    <div className="border-b border-border">
      <nav className="flex space-x-8 overflow-x-auto">
        {filteredItems.map((item) => {
          const isActive = pathname === item.href;

          return (
            <Link
              key={item.key}
              href={item.href}
              className={cn(
                "whitespace-nowrap border-b-2 py-4 px-1 text-md font-bold transition-colors",
                isActive
                  ? "border-primary text-primary"
                  : "border-transparent text-muted-foreground hover:text-foreground hover:border-muted-foreground"
              )}
            >
              {item.label}
            </Link>
          );
        })}
      </nav>
    </div>
  );
}
