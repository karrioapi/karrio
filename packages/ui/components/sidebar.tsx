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
  Building2,
  BarChart3,
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
  ];

  // Resources items (moved from submenu to main nav)
  const productItems = [
    {
      title: "Connections",
      url: "/connections",
      icon: List,
    },
    ...(metadata?.SHIPPING_RULES || metadata?.WORKFLOW_MANAGEMENT ? [{
      title: "Automation",
      url: metadata?.SHIPPING_RULES ? "/shipping-rules" : "/workflows",
      icon: Zap,
    }] : []),
    ...(metadata?.ADVANCED_ANALYTICS ? [{
      title: "Reports",
      url: "/reports",
      icon: BarChart3,
    }] : []),
    ...(metadata?.ADMIN_DASHBOARD && user?.is_staff ? [{
      title: "Control",
      url: "/admin",
      icon: Shield,
    }] : []),
    ...(metadata?.MULTI_ORGANIZATIONS && user?.is_superuser ? [{
      title: "Shippers",
      url: "/shippers",
      icon: Building2,
      items: [
        {
          title: "Overview",
          url: "/shippers/overview",
        },
        {
          title: "Accounts",
          url: "/shippers/accounts",
        },
        {
          title: "Markups",
          url: "/shippers/markups",
        },
      ],
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
        {productItems.length > 0 && <NavMain items={productItems} label="Products" />}
      </SidebarContent>
      <SidebarFooter>
        <SidebarMenu>
          <SidebarMenuItem className="hidden lg:block">
            <SidebarMenuButton
              onClick={() => {
                const event = new CustomEvent('toggle-developer-tools');
                window.dispatchEvent(event);
              }}
              tooltip="Developer Tools"
            >
              <Terminal className="size-4" />
              <span>Developers</span>
            </SidebarMenuButton>
          </SidebarMenuItem>
        </SidebarMenu>
      </SidebarFooter>
      <SidebarRail />
    </Sidebar>
  )
}
