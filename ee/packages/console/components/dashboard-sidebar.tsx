"use client";

import * as React from "react";
import {
  Building2,
  CreditCard,
  FileCode,
  Folder,
  LayoutGrid,
  Settings,
  Users,
} from "lucide-react";
import {
  Sidebar,
  SidebarContent,
  SidebarFooter,
  SidebarHeader,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
  SidebarRail,
} from "@karrio/insiders/components/ui/sidebar";
import { NavProjects } from "@karrio/console/components/nav-projects";
import { OrgSwitcher } from "@karrio/console/components/org-switcher";
import { NavMain } from "@karrio/console/components/nav-main";
import { NavUser } from "@karrio/console/components/nav-user";
import { trpc } from "@karrio/console/trpc/client";
import { useParams } from "next/navigation";
import Image from "next/image";

// This is sample data.
const data = {
  navMain: [
    {
      name: "Projects",
      url: (orgId: string) => `/orgs/${orgId}`,
      icon: Building2,
    },
    {
      name: "Billing",
      url: (orgId: string) => `/orgs/${orgId}/billing`,
      icon: CreditCard,
    },
    {
      name: "Settings",
      url: (orgId: string) => `/orgs/${orgId}/settings`,
      icon: Settings,
    },
  ],
  projects: [
    {
      name: "Overview",
      url: (orgId: string, projectId: string) =>
        `/orgs/${orgId}/projects/${projectId}`,
      icon: LayoutGrid,
    },
    {
      name: "Accounts",
      url: (orgId: string, projectId: string) =>
        `/orgs/${orgId}/projects/${projectId}/accounts`,
      icon: Users,
    },
    {
      name: "Settings",
      url: (orgId: string, projectId: string) =>
        `/orgs/${orgId}/projects/${projectId}/settings`,
      icon: Settings,
    },
  ],
};

export function DashboardSidebar({
  ...props
}: React.ComponentProps<typeof Sidebar>) {
  const params = useParams();
  const orgId = params?.orgId as string;
  const projectId = params?.projectId as string;
  const { data: user } = trpc.users.get.useQuery();

  return (
    <Sidebar collapsible="icon" className="sidebar-root" {...props}>
      <SidebarHeader className="sidebar-header">
        <SidebarMenu>
          <SidebarMenuItem>
            <SidebarMenuButton size="lg" asChild>
              <a href="/orgs">
                <div className="flex aspect-square size-8 items-center justify-center rounded-lg bg-sidebar-primary text-sidebar-primary-foreground">
                  <Image
                    className="h-8 w-8"
                    src="/icon.svg"
                    alt="Karrio Logo"
                    width={24}
                    height={24}
                  />
                </div>
              </a>
            </SidebarMenuButton>
          </SidebarMenuItem>
          {!orgId && (
            <SidebarMenuItem>
              <SidebarMenuButton asChild>
                <a href="/orgs">
                  <Folder />
                  <span>Organizations</span>
                </a>
              </SidebarMenuButton>
            </SidebarMenuItem>
          )}
        </SidebarMenu>

        {orgId && <OrgSwitcher selectedOrgId={orgId} />}
      </SidebarHeader>

      <SidebarContent className="sidebar-content">
        {projectId && <NavProjects projects={data.projects} />}
        {orgId && !projectId && <NavMain items={data.navMain} />}
      </SidebarContent>

      <SidebarFooter className="sidebar-footer">
        <NavUser user={user as any} />
      </SidebarFooter>

      <SidebarRail className="sidebar-rail" />
    </Sidebar>
  );
}
