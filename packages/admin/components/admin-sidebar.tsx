"use client";

import {
  Box,
  Building2,
  Clock,
  FileText,
  LayoutDashboard,
  Truck,
  Users,
} from "lucide-react";
import { usePathname } from "next/navigation";
import { cn } from "@karrio/ui/lib/utils";
import Link from "next/link";
import { useAPIMetadata } from "@karrio/hooks/api-metadata";
import { useEffect, useState } from "react";

const menuItems = [
  {
    label: "Platform console",
    icon: LayoutDashboard,
    href: "/admin",
  },
  {
    label: "Staff and permissions",
    icon: Users,
    href: "/admin/staff",
  },
  {
    label: "Carriers network",
    icon: Truck,
    href: "/admin/carriers",
  },
  {
    label: "Connected accounts",
    icon: Building2,
    href: "/admin/accounts",
  },
  {
    label: "Shipping add-ons",
    icon: FileText,
    href: "/admin/addons",
    isDisabled: true,
  },
  {
    label: "Activity log",
    icon: Clock,
    href: "/admin/activity",
    isDisabled: true,
  },
];

export function AdminSidebar({ isDrawer }: { isDrawer?: boolean }) {
  const pathname = usePathname();
  const basePath = pathname?.split("/admin")[0] || "";
  const { metadata } = useAPIMetadata();
  const [appHost, setAppHost] = useState("");

  useEffect(() => {
    setAppHost(window && window.location.host);
  }, []);

  return (
    <div className={cn(!isDrawer && "rounded-lg border bg-white shadow-sm h-fit")}>
      {!isDrawer && <div className="flex h-14 items-center gap-3 border-b px-4">
        <div className="flex h-8 w-8 items-center justify-center rounded bg-primary">
          <Box className="h-5 w-5 text-white" />
        </div>
        <div className="flex flex-col">
          <span className="text-sm font-medium">{metadata.APP_NAME}</span>
          <span className="text-xs text-muted-foreground">{appHost}</span>
        </div>
      </div>}
      <div className="px-2 py-4">
        {menuItems.map((item) => (
          <Link
            key={item.label}
            href={`${basePath}${item.href}`}
            className={cn(
              "flex items-center gap-3 rounded-md px-2 py-2 text-sm text-gray-700 hover:bg-gray-100",
              "focus-visible:bg-gray-100 focus-visible:outline-none",
              pathname === `${basePath}${item.href}` &&
              "bg-gray-100 font-medium",
              item.isDisabled && "pointer-events-none opacity-50",
            )}
          >
            <item.icon className="h-4 w-4" />
            {item.label}
          </Link>
        ))}
      </div>
    </div>
  );
}
