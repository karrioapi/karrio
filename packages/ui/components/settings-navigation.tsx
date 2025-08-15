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
    label: "Account details",
    href: "/settings/account",
  },
  {
    key: "profile",
    label: "Personal details",
    href: "/settings/profile",
  },
  {
    key: "organization",
    label: "Team and security",
    href: "/settings/organization",
    requiresOrg: true,
  },
  {
    key: "addresses",
    label: "Location & addresses",
    href: "/settings/addresses",
  },
  {
    key: "parcels",
    label: "Parcel presets",
    href: "/settings/parcels",
  },
  {
    key: "templates",
    label: "Document templates",
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
