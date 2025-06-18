"use client"

import * as React from "react"
import { ChevronsUpDown, Plus, Building } from "lucide-react"
import {
  OrganizationType,
  useOrganizationMutation,
  useOrganizations,
} from "@karrio/hooks/organization";
import { useCreateOrganizationModal } from "@karrio/ui/core/modals/create-organization-modal";
import { useAcceptInvitation } from "@karrio/ui/core/modals/accept-invitation-modal";
import { useAPIMetadata } from "@karrio/hooks/api-metadata";
import { useAPIToken } from "@karrio/hooks/api-token";
import { useSearchParams } from "next/navigation";
import { useLoader } from "@karrio/ui/core/components/loader";
import { isNoneOrEmpty } from "@karrio/lib";
import { p } from "@karrio/lib";
import Image from "next/image";

import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuShortcut,
  DropdownMenuTrigger,
} from "@karrio/ui/components/ui/dropdown-menu"
import {
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
  useSidebar,
} from "@karrio/ui/components/ui/sidebar"

export function TeamSwitcher() {
  const { isMobile } = useSidebar();
  const searchParams = useSearchParams();
  const { query } = useAPIToken();
  const mutation = useOrganizationMutation();
  const { setLoading } = useLoader();
  const { organizations, organization } = useOrganizations();
  const {
    metadata: { ALLOW_MULTI_ACCOUNT },
  } = useAPIMetadata();
  const { acceptInvitation } = useAcceptInvitation();
  const { createOrganization } = useCreateOrganizationModal();
  const [initialized, setInitialized] = React.useState<boolean>(false);

  const select = (org: OrganizationType) => async (e: any) => {
    e.preventDefault();
    e.stopPropagation();

    if (org.id === organization?.id) return;
    setLoading(true);
    try {
      await mutation.changeActiveOrganization(org.id);
    } finally {
      setLoading(false);
    }
  };

  const create = async () => {
    createOrganization({
      onChange: (orgId: string) => {
        return mutation.changeActiveOrganization(orgId);
      },
    });
  };

  React.useEffect(() => {
    if (!initialized && !isNoneOrEmpty(searchParams.get("accept_invitation"))) {
      acceptInvitation({
        onChange: (orgId) => mutation.changeActiveOrganization(orgId),
      });
      setInitialized(true);
    }
    if (searchParams && isNoneOrEmpty(searchParams.get("accept_invitation"))) {
      setInitialized(true);
    }
  }, [initialized, searchParams, acceptInvitation, mutation]);

  // Show fallback logo if no organizations
  if (query.isFetched && (organizations || []).length === 0) {
    return (
      <SidebarMenu>
        <SidebarMenuItem>
          <div className="p-2">
            <Image
              src={p`/icon.svg`}
              width={24}
              height={24}
              alt="logo"
            />
          </div>
        </SidebarMenuItem>
      </SidebarMenu>
    );
  }

  // Don't render if no organizations yet
  if (!organization || (organizations || []).length === 0) {
    return null;
  }

  return (
    <SidebarMenu>
      <SidebarMenuItem>
        <DropdownMenu>
          <DropdownMenuTrigger asChild>
            <SidebarMenuButton
              size="lg"
              className="data-[state=open]:bg-sidebar-accent data-[state=open]:text-sidebar-accent-foreground"
            >
              <div className="flex aspect-square size-8 items-center justify-center rounded-lg bg-sidebar-primary text-sidebar-primary-foreground">
                <Building className="size-4" />
              </div>
              <div className="grid flex-1 text-left text-sm leading-tight">
                <span className="truncate font-semibold">{organization.name}</span>
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
            <DropdownMenuLabel className="text-xs text-muted-foreground">
              Organizations
            </DropdownMenuLabel>
            {(organizations || []).map((org, index) => (
              <DropdownMenuItem
                key={`org-${org.id}`}
                onClick={select(org)}
                className="gap-2 p-2"
              >
                <div className="flex size-6 items-center justify-center rounded-sm border">
                  <Building className="size-4 shrink-0" />
                </div>
                <span className="flex-1 truncate">{org.name}</span>
                {org.id === organization?.id && (
                  <div className="size-2 rounded-full bg-blue-500" />
                )}
                <DropdownMenuShortcut>⌘{index + 1}</DropdownMenuShortcut>
              </DropdownMenuItem>
            ))}
            {ALLOW_MULTI_ACCOUNT && (
              <>
                <DropdownMenuSeparator />
                <DropdownMenuItem onClick={create} className="gap-2 p-2">
                  <div className="flex size-6 items-center justify-center rounded-md border bg-background">
                    <Plus className="size-4" />
                  </div>
                  <div className="font-medium text-muted-foreground">New organization</div>
                </DropdownMenuItem>
              </>
            )}
          </DropdownMenuContent>
        </DropdownMenu>
      </SidebarMenuItem>
    </SidebarMenu>
  )
}
