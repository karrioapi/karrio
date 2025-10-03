"use client";

import * as React from "react";
import { ChevronsUpDown, Plus, Building2 } from "lucide-react";
import { Organization } from "@karrio/console/types/next-auth";
import { trpc } from "@karrio/console/trpc/client";
import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuShortcut,
  DropdownMenuTrigger,
} from "@karrio/ui/components/ui/dropdown-menu";
import {
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
  useSidebar,
} from "@karrio/ui/components/ui/sidebar";

export function OrgSwitcher({ selectedOrgId }: { selectedOrgId?: string }) {
  const { isMobile } = useSidebar();
  const router = useRouter();
  const { data: organizations } = trpc.organizations.getAll.useQuery();
  const [activeOrg, setActiveOrg] = useState<Organization | null>(null);

  useEffect(() => {
    if (organizations && selectedOrgId) {
      const currentOrg = organizations.find(
        (org: any) => org.id === selectedOrgId,
      );
      setActiveOrg(currentOrg || (organizations[0] as any));
    }
  }, [organizations, selectedOrgId]);

  const handleOrgSelect = (org: Organization) => {
    setActiveOrg(org);
    router.push(`/orgs/${org.id}`);
  };

  return (
    <SidebarMenu>
      <SidebarMenuItem>
        <DropdownMenu>
          <DropdownMenuTrigger asChild>
            <SidebarMenuButton
              size="lg"
              className="data-[state=open]:bg-sidebar-accent data-[state=open]:text-sidebar-accent-foreground"
              tooltip={activeOrg?.name || "Select Organization"}
            >
              <div className="flex aspect-square size-8 items-center justify-center rounded-lg bg-sidebar-primary text-sidebar-primary-foreground">
                <Building2 className="size-4" />
              </div>
              <div className="grid flex-1 text-left text-sm leading-tight">
                <span className="truncate font-semibold">
                  {activeOrg?.name || "Select Organization"}
                </span>
              </div>
              <ChevronsUpDown className="ml-auto" />
            </SidebarMenuButton>
          </DropdownMenuTrigger>
          <DropdownMenuContent
            className="w-[--radix-dropdown-menu-trigger-width] min-w-56 rounded-lg"
            align="start"
            side={isMobile ? "bottom" : "right"}
            sideOffset={4}
          >
            {organizations && organizations.length > 0 && (
              <>
                {!selectedOrgId && (
                  <>
                    <DropdownMenuItem className="gap-2 p-2 text-muted-foreground">
                      Select an Organization
                    </DropdownMenuItem>
                    <DropdownMenuSeparator />
                  </>
                )}
                {organizations?.map((org: any, index: number) => (
                  <DropdownMenuItem
                    key={org.id}
                    onClick={() => handleOrgSelect(org as any)}
                    className="gap-2 p-2"
                  >
                    <div className="flex size-6 items-center justify-center rounded-sm border">
                      <Building2 className="size-4 shrink-0" />
                    </div>
                    {org.name}
                    <DropdownMenuShortcut>⌘{index + 1}</DropdownMenuShortcut>
                  </DropdownMenuItem>
                ))}
                <DropdownMenuSeparator />
              </>
            )}
            <DropdownMenuLabel className="text-xs text-muted-foreground">
              Actions
            </DropdownMenuLabel>
            <DropdownMenuItem
              className="gap-2 p-2"
              onClick={() => router.push("/orgs/create")}
            >
              <div className="flex size-6 items-center justify-center rounded-md border bg-background">
                <Plus className="size-4" />
              </div>
              <div className="font-medium text-muted-foreground">
                Create new organization
              </div>
            </DropdownMenuItem>
          </DropdownMenuContent>
        </DropdownMenu>
      </SidebarMenuItem>
    </SidebarMenu>
  );
}
