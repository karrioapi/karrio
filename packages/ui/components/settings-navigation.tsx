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
    <nav className="flex space-x-8 overflow-x-auto">
      {filteredItems.map((item) => {
        const isActive = pathname === item.href;

        return (
          <Link
            key={item.key}
            href={item.href}
            className={cn(
              "whitespace-nowrap border-b-2 py-4 px-1 text-sm font-medium transition-colors",
              isActive
                ? "border-purple-500 text-purple-600"
                : "border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300"
            )}
          >
            {item.label}
          </Link>
        );
      })}
    </nav>
  );
}
