"use client";

import * as React from "react";
import {
  Building2,
  CreditCard,
  FileCode,
  Folder,
  LayoutGrid,
  Server,
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
} from "@karrio/ui/components/ui/sidebar";
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
      icon: Server,
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
    <Sidebar collapsible="icon" {...props}>
      <SidebarHeader>
        <SidebarMenu>
          <SidebarMenuItem>
            <SidebarMenuButton size="lg" asChild tooltip="Karrio">
              <a href="/orgs">
                <div className="flex aspect-square size-8 items-center justify-center rounded-lg bg-sidebar-primary text-sidebar-primary-foreground">
                  <Image
                    className="h-6 w-6"
                    src="/icon.svg"
                    alt="Karrio Logo"
                    width={24}
                    height={24}
                  />
                </div>
                <div className="grid flex-1 text-left text-sm leading-tight">
                  <span className="truncate font-semibold">Karrio</span>
                </div>
              </a>
            </SidebarMenuButton>
          </SidebarMenuItem>
          {!orgId && (
            <SidebarMenuItem>
              <SidebarMenuButton asChild tooltip="Organizations">
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

      <SidebarContent>
        {projectId && <NavProjects projects={data.projects} />}
        {orgId && !projectId && <NavMain items={data.navMain} />}
      </SidebarContent>

      <SidebarFooter>
        <NavUser user={user as any} />
      </SidebarFooter>

      <SidebarRail />
    </Sidebar>
  );
}
