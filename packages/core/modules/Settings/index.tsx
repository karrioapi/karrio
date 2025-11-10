"use client";

import * as React from "react";
import { AppLink } from "@karrio/ui/core/components/app-link";
import {
  User,
  Building2,
  Users,
  MapPin,
  Package,
  FileText,
} from "lucide-react";
import { Card, CardContent } from "@karrio/ui/components/ui/card";
import { useAPIMetadata } from "@karrio/hooks/api-metadata";

interface SettingItem {
  title: string;
  description: string;
  icon: React.ComponentType<{ className?: string }>;
  href: string;
}

interface SettingSection {
  title: string;
  items: SettingItem[];
}

const settingSections: SettingSection[] = [
  {
    title: "Account settings",
    items: [
      {
        title: "Personal details",
        description: "Personal details, password, and active sessions.",
        icon: User,
        href: "/settings/profile",
      },
      {
        title: "Account details",
        description: "Account shipping preferences, print settings, and more.",
        icon: Building2,
        href: "/settings/account",
      },
      {
        title: "Team and security",
        description: "Team members, roles, and account security.",
        icon: Users,
        href: "/settings/organization",
      },
    ],
  },
  {
    title: "Workspace settings",
    items: [
      {
        title: "Location & addresses",
        description: "Manage your business locations, shipping addresses, and warehouse information.",
        icon: MapPin,
        href: "/settings/addresses",
      },
      {
        title: "Parcel presets",
        description: "Create and manage parcel templates for faster shipping operations.",
        icon: Package,
        href: "/settings/parcels",
      },
      {
        title: "Document templates",
        description: "Customize shipping labels, invoices, and other document templates.",
        icon: FileText,
        href: "/settings/templates",
      },
    ],
  },
];

function SettingCard({ item }: { item: SettingItem }) {
  const Icon = item.icon;

  return (
    <AppLink href={item.href} className="block h-full">
      <Card className="cursor-pointer transition-colors hover:border-gray-300 group h-full border border-gray-200 shadow-none">
        <CardContent className="p-4 h-full flex flex-col">
          <div className="flex items-start gap-3 flex-1">
            <div className="flex-shrink-0 p-2 bg-gray-50 rounded-md group-hover:bg-gray-100 transition-colors">
              <Icon className="h-5 w-5 text-gray-600" />
            </div>
            <div className="flex-1 min-w-0">
              <h3 className="font-medium text-sm text-gray-900 group-hover:text-blue-600 transition-colors">
                {item.title}
              </h3>
              <p className="text-sm text-gray-500 mt-0.5 leading-relaxed">
                {item.description}
              </p>
            </div>
          </div>
        </CardContent>
      </Card>
    </AppLink>
  );
}

export default function Settings() {
  const { metadata } = useAPIMetadata();

  // Filter out "Team and security" if MULTI_ORGANIZATIONS is false
  const filteredSections = React.useMemo(() => {
    return settingSections.map(section => ({
      ...section,
      items: section.items.filter(item => {
        if (item.title === "Team and security" && !metadata?.MULTI_ORGANIZATIONS) {
          return false;
        }
        return true;
      })
    })).filter(section => section.items.length > 0);
  }, [metadata?.MULTI_ORGANIZATIONS]);

  return (
    <div>
      <div className="mb-6">
        <h1 className="text-2xl font-semibold text-gray-900">Settings</h1>
      </div>

      <div className="space-y-8">
        {filteredSections.map((section) => (
          <div key={section.title}>
            <h2 className="text-lg font-medium text-gray-900 mb-3">
              {section.title}
            </h2>
            <div className="grid gap-4 grid-cols-1 sm:grid-cols-2 lg:grid-cols-3">
              {section.items.map((item) => (
                <SettingCard key={item.title} item={item} />
              ))}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
