"use client";

import { type LucideIcon } from "lucide-react";
import {
  SidebarGroup,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
} from "@karrio/insiders/components/ui/sidebar";
import { useParams } from "next/navigation";

export function NavProjects({
  projects,
}: {
  projects: {
    name: string;
    url: (orgId: string, projectId: string) => string;
    icon: LucideIcon;
  }[];
}) {
  const { orgId, projectId } = useParams();

  return (
    <SidebarGroup className="group-data-[collapsible=icon]:hidden">
      <SidebarMenu>
        {projects.map((item) => (
          <SidebarMenuItem key={item.name}>
            <SidebarMenuButton asChild>
              <a href={item.url(orgId as string, projectId as string)}>
                <item.icon />
                <span>{item.name}</span>
              </a>
            </SidebarMenuButton>
          </SidebarMenuItem>
        ))}
      </SidebarMenu>
    </SidebarGroup>
  );
}
