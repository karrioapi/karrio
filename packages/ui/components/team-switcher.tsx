"use client"

import * as React from "react"
import { ChevronsUpDown, Plus, Building, Check } from "lucide-react"
import {
  OrganizationType,
  useOrganizationMutation,
  useOrganizations,
} from "@karrio/hooks/organization";
import { useCreateOrganizationDialog } from "@karrio/ui/components/create-organization-dialog";
import { useAcceptInvitationDialog } from "@karrio/ui/components/accept-invitation-dialog";
import { useLoader } from "@karrio/ui/core/components/loader";
import { useAPIMetadata } from "@karrio/hooks/api-metadata";
import { useAPIToken } from "@karrio/hooks/api-token";
import { useSearchParams } from "next/navigation";
import { isNoneOrEmpty } from "@karrio/lib";
import { p } from "@karrio/lib";
import { cn } from "@karrio/ui/lib/utils";
import Image from "next/image";

import {
  Command,
  CommandEmpty,
  CommandGroup,
  CommandInput,
  CommandItem,
  CommandList,
  CommandSeparator,
} from "@karrio/ui/components/ui/command"
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "@karrio/ui/components/ui/popover"
import {
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
  useSidebar,
} from "@karrio/ui/components/ui/sidebar"

export function TeamSwitcher() {
  const { isMobile } = useSidebar();
  const {
    metadata: { ALLOW_MULTI_ACCOUNT, MULTI_ORGANIZATIONS },
  } = useAPIMetadata();

  // Logo fallback - only show when multi-org is NOT supported
  const renderLogoFallback = () => (
    <SidebarMenu>
      <SidebarMenuItem>
        <div className="p-2 flex items-center gap-2">
          <Image
            src={p`/icon.svg`}
            width={24}
            height={24}
            alt="Karrio"
          />
        </div>
      </SidebarMenuItem>
    </SidebarMenu>
  );

  // Early return if multi-organizations is disabled
  if (!MULTI_ORGANIZATIONS) {
    return renderLogoFallback();
  }

  // Only call organization-related hooks when multi-organizations is enabled
  const searchParams = useSearchParams();
  const { query } = useAPIToken();
  const mutation = useOrganizationMutation();
  const { setLoading } = useLoader();
  const { organizations, organization } = useOrganizations();
  const { acceptInvitation } = useAcceptInvitationDialog();
  const { createOrganization } = useCreateOrganizationDialog();
  const [initialized, setInitialized] = React.useState<boolean>(false);
  const [open, setOpen] = React.useState(false);

  const select = (org: OrganizationType) => async () => {
    if (org.id === organization?.id) return;
    setLoading(true);
    try {
      await mutation.changeActiveOrganization(org.id);
      setOpen(false);
    } finally {
      setLoading(false);
    }
  };

  const create = async () => {
    setOpen(false);
    createOrganization({
      onChange: (orgId: string) => {
        return mutation.changeActiveOrganization(orgId);
      },
    });
  };

  React.useEffect(() => {
    if (!initialized && !isNoneOrEmpty(searchParams.get("accept_invitation"))) {
      acceptInvitation();
      setInitialized(true);
    }
    if (searchParams && isNoneOrEmpty(searchParams.get("accept_invitation"))) {
      setInitialized(true);
    }
  }, [initialized, searchParams, acceptInvitation, mutation]);

  // Placeholder skeleton animation for loading states
  const renderPlaceholder = () => (
    <SidebarMenu>
      <SidebarMenuItem>
        <div className="p-2 flex items-center gap-2">
          <div className="flex aspect-square size-8 items-center justify-center rounded-lg bg-muted animate-pulse">
            <div className="size-4 bg-muted-foreground/20 rounded" />
          </div>
          <div className="flex-1">
            <div className="h-4 bg-muted animate-pulse rounded w-24" />
          </div>
        </div>
      </SidebarMenuItem>
    </SidebarMenu>
  );

  // Loading state - show placeholder animation
  if (query.isLoading) {
    return renderPlaceholder();
  }

  // Error state - show placeholder animation
  if (query.error) {
    return renderPlaceholder();
  }

  // Check if everything is loaded and multi-org is NOT supported
  const isFullyLoaded = query.isFetched;
  const isMultiOrgDisabled = !ALLOW_MULTI_ACCOUNT;
  const hasNoOrganizations = (organizations || []).length === 0;

  // Show logo only when fully loaded, multi-org disabled, and no organizations
  if (isFullyLoaded && isMultiOrgDisabled && hasNoOrganizations) {
    return renderLogoFallback();
  }

  // Show placeholder if not fully loaded yet
  if (!isFullyLoaded) {
    return renderPlaceholder();
  }

  // Show organization combobox if we have organizations
  if ((organizations || []).length > 0) {
    const currentOrg = organization || organizations![0];
    return (
      <SidebarMenu>
        <SidebarMenuItem>
          <Popover open={open} onOpenChange={setOpen}>
            <PopoverTrigger asChild>
              <SidebarMenuButton
                size="lg"
                role="combobox"
                aria-expanded={open}
                className="data-[state=open]:bg-sidebar-accent data-[state=open]:text-sidebar-accent-foreground"
              >
                <div className="flex aspect-square size-8 items-center justify-center rounded-lg bg-muted text-muted-foreground">
                  <Building className="size-4" />
                </div>
                <div className="grid flex-1 text-left text-sm leading-tight">
                  <span className="truncate font-semibold">{currentOrg.name}</span>
                </div>
                <ChevronsUpDown className="ml-auto size-4 shrink-0 opacity-50" />
              </SidebarMenuButton>
            </PopoverTrigger>
            <PopoverContent
              className="w-[--radix-popover-trigger-width] min-w-56 p-0"
              align="start"
              side="bottom"
              sideOffset={4}
            >
              <Command>
                <CommandList>
                  <CommandEmpty>No organizations found.</CommandEmpty>
                  <CommandGroup heading="Organizations">
                    {organizations!.map((org, index) => (
                      <CommandItem
                        key={`org-${org.id}`}
                        value={org.name}
                        onSelect={() => select(org)()}
                      >
                        <div className="flex size-6 items-center justify-center rounded-sm border bg-muted text-muted-foreground">
                          <Building className="size-4 shrink-0" />
                        </div>
                        <span className="flex-1 truncate">{org.name}</span>
                        <Check
                          className={cn(
                            "size-4",
                            org.id === currentOrg.id ? "opacity-100" : "opacity-0"
                          )}
                        />
                        <span className="ml-2 text-xs text-muted-foreground">⌘{index + 1}</span>
                      </CommandItem>
                    ))}
                  </CommandGroup>
                  {ALLOW_MULTI_ACCOUNT && (
                    <>
                      <CommandSeparator />
                      <CommandGroup>
                        <CommandItem onSelect={create}>
                          <div className="flex size-6 items-center justify-center rounded-md border bg-background">
                            <Plus className="size-4" />
                          </div>
                          <span className="font-medium text-muted-foreground">New organization</span>
                        </CommandItem>
                      </CommandGroup>
                    </>
                  )}
                </CommandList>
              </Command>
            </PopoverContent>
          </Popover>
        </SidebarMenuItem>
      </SidebarMenu>
    );
  }

  // Final fallback - show placeholder animation
  return renderPlaceholder();
}
