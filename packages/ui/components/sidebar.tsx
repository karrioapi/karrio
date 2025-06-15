"use client"

import * as React from "react"
import {
  Home,
  Truck,
  MapPin,
  Package,
  Settings,
  Users,
  Zap,
  Puzzle,
  Terminal,
  Building,
  Shield,
  Book,
  Inbox,
  List,
} from "lucide-react"

import { NavMain } from "@karrio/ui/components/nav-main"
import { TeamSwitcher } from "@karrio/ui/components/team-switcher"
import {
  Sidebar,
  SidebarContent,
  SidebarFooter,
  SidebarHeader,
  SidebarRail,
  useSidebar,
} from "@karrio/ui/components/ui/sidebar"
import { useAPIMetadata } from "@karrio/hooks/api-metadata"
import { useUser } from "@karrio/hooks/user"
import { useAppMode } from "@karrio/hooks/app-mode"

export function AppSidebar({ ...props }: React.ComponentProps<typeof Sidebar>) {
  const { metadata } = useAPIMetadata();
  const { testMode } = useAppMode();
  const {
    query: { data: { user } = {} },
  } = useUser();

  // Navigation items based on Karrio features - matching expanded-sidebar.tsx exactly
  const navMain = [
    {
      title: "Home",
      url: "/",
      icon: Home,
    },
    {
      title: "Shipments",
      url: "/shipments",
      icon: Truck,
    },
    {
      title: "Trackers",
      url: "/trackers",
      icon: MapPin,
    },
    ...(metadata?.ORDERS_MANAGEMENT ? [{
      title: "Orders",
      url: "/orders",
      icon: Inbox,
    }] : []),
    {
      title: "Carriers",
      url: "/connections",
      icon: List,
    },
    ...(metadata?.SHIPPING_RULES || metadata?.WORKFLOW_MANAGEMENT ? [{
      title: "Automation",
      url: metadata?.SHIPPING_RULES ? "/shipping-rules" : "/workflows",
      icon: Zap,
    }] : []),
    {
      title: "Settings",
      url: "/settings/account",
      icon: Settings,
    },
  ];

  // Separate section for developers and resources
  const developerItems = [
    ...(metadata?.APPS_MANAGEMENT ? [{
      title: "App Store",
      url: "/app-store",
      icon: Puzzle,
    }] : []),
    {
      title: "Developers",
      url: "/developers",
      icon: Terminal,
    },
    {
      title: "Resources",
      url: "/resources",
      icon: Book,
      items: [
        {
          title: "Playground",
          url: "/resources/playground",
        },
        {
          title: "GraphiQL",
          url: "/resources/graphiql",
        },
        ...(metadata?.APP_NAME?.includes("Karrio") ? [{
          title: "Guides",
          url: "https://docs.karrio.io",
          external: true,
        }] : []),
      ],
    },
    ...(metadata?.ADMIN_DASHBOARD && user?.is_staff ? [{
      title: "Administration",
      url: "/admin",
      icon: Shield,
    }] : []),
  ];

  return (
    <Sidebar
      collapsible="icon"
      {...props}
      className={testMode ? "mt-[4px]" : ""}
    >
      <SidebarHeader>
        <TeamSwitcher />
      </SidebarHeader>
      <SidebarContent>
        <NavMain items={navMain} />
        <NavMain items={developerItems} label="Resources" />
      </SidebarContent>
      <SidebarFooter>
        {/* Footer content removed - user menu is in navbar */}
      </SidebarFooter>
      <SidebarRail />
    </Sidebar>
  )
}
