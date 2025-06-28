"use client"

import * as React from "react"
import {
  Home,
  Truck,
  MapPin,
  Settings,
  Zap,
  Code2,
  Terminal,
  Shield,
  BookOpen,
  Inbox,
  List,
  Brackets,
} from "lucide-react"


import { NavMain } from "@karrio/ui/components/nav-main"
import { TeamSwitcher } from "@karrio/ui/components/team-switcher"
import {
  Sidebar,
  SidebarContent,
  SidebarFooter,
  SidebarHeader,
  SidebarRail,
  SidebarMenu,
  SidebarMenuItem,
  SidebarMenuButton,
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

  // Resources items (moved from submenu to main nav)
  const resourceItems = [
    {
      title: "Playground",
      url: "/resources/playground",
      icon: Code2, // Better icon for Swagger/API playground
    },
    {
      title: "GraphiQL",
      url: "/resources/graphiql",
      icon: Brackets, // More appropriate for GraphQL interface
    },
    ...(metadata?.APP_NAME?.includes("Karrio") ? [{
      title: "Guides",
      url: "https://karrio.io/docs",
      icon: BookOpen, // More appropriate for documentation
      external: true,
    }] : []),
  ];

  // Admin and developer tools
  const bottomItems = [
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
        <NavMain items={resourceItems} label="Resources" />
        <NavMain items={bottomItems} label="Admin" />
      </SidebarContent>
      <SidebarFooter>
        <SidebarMenu>
          <SidebarMenuItem>
            <SidebarMenuButton
              onClick={() => {
                // This will be handled by the provider context
                const event = new CustomEvent('toggle-developer-tools');
                window.dispatchEvent(event);
              }}
            >
              <Terminal />
              <span>Developer Tools</span>
            </SidebarMenuButton>
          </SidebarMenuItem>
        </SidebarMenu>
      </SidebarFooter>
      <SidebarRail />
    </Sidebar>
  )
}
