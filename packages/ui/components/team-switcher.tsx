"use client"

import * as React from "react"
import { ChevronsUpDown, Plus, Building, Settings, LogOut, User } from "lucide-react"
import { useAppMode } from "@karrio/hooks/app-mode"
import { useUser } from "@karrio/hooks/user"
import { signOut } from "next-auth/react"
import { AppLink } from "@karrio/ui/core/components/app-link"
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
import Image from "next/image";
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "@karrio/ui/components/ui/popover"
import {
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
} from "@karrio/ui/components/ui/sidebar"

export function TeamSwitcher() {
  const { query: userQuery } = useUser();
  const { testMode } = useAppMode();
  const {
    metadata: { ALLOW_MULTI_ACCOUNT, MULTI_ORGANIZATIONS },
  } = useAPIMetadata();

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

  const user = userQuery.data?.user;

  const select = (org: OrganizationType) => async () => {
    if (org.id === organization?.id) return;
    setLoading(true);
    try {
      await mutation.changeActiveOrganization(org.id);
      // Soft refresh to re-render server components using new orgId
      if (typeof window !== 'undefined') {
        try {
          // App Router-friendly refresh
          // eslint-disable-next-line @typescript-eslint/ban-ts-comment
          // @ts-ignore
          if (window.next && window.next.router) {
            // legacy fallback
            window.location.reload();
          } else {
            window.location.reload();
          }
        } catch {
          window.location.reload();
        }
      }
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

  // Show placeholder if not fully loaded yet
  if (!query.isFetched) {
    return renderPlaceholder();
  }

  // Render dropdown for multi-org disabled scenario
  if (!MULTI_ORGANIZATIONS) {
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
                  <Image
                    src={p`/icon.svg`}
                    width={16}
                    height={16}
                    alt="Karrio"
                  />
                </div>
                <div className="grid flex-1 text-left text-sm leading-tight">
                  <span className="truncate font-semibold">Karrio</span>
                </div>
                <ChevronsUpDown className="ml-auto size-4 shrink-0 opacity-50" />
              </SidebarMenuButton>
            </PopoverTrigger>
            <PopoverContent
              className="w-[320px] p-0"
              align="start"
              side="bottom"
              sideOffset={4}
            >
              <div className="p-0">
                {/* Settings */}
                <div className="p-3 border-b">
                  <AppLink
                    href="/settings"
                    className="w-full flex items-center gap-3 px-3 py-2 text-sm text-left rounded-md hover:bg-muted transition-colors"
                    onClick={() => setOpen(false)}
                  >
                    <Settings className="size-4 text-muted-foreground" />
                    <span>Settings</span>
                  </AppLink>
                </div>

                {/* User Section */}
                <div className="p-3">
                  <AppLink
                    href="/settings/profile"
                    className="w-full flex items-center gap-3 px-3 py-2 text-sm text-left rounded-md hover:bg-muted transition-colors"
                    onClick={() => setOpen(false)}
                  >
                    <User className="size-4 text-muted-foreground" />
                    <span>{user?.full_name || user?.email || "Profile"}</span>
                  </AppLink>
                  <button
                    onClick={() => {
                      setOpen(false);
                      signOut({ callbackUrl: "/" });
                    }}
                    className="w-full flex items-center gap-3 px-3 py-2 text-sm text-left rounded-md hover:bg-muted transition-colors text-red-600 hover:text-red-700"
                  >
                    <LogOut className="size-4" />
                    <span>Sign out</span>
                  </button>
                </div>
              </div>
            </PopoverContent>
          </Popover>
        </SidebarMenuItem>
      </SidebarMenu>
    );
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
              className="w-[320px] p-0"
              align="start"
              side="bottom"
              sideOffset={4}
            >
              <div className="p-0">
                {/* Current Organization Section */}
                <div className="p-4 border-b">
                  <div className="flex items-center gap-3">
                    <div className="flex aspect-square size-10 items-center justify-center rounded-lg bg-primary text-primary-foreground">
                      <Building className="size-5" />
                    </div>
                    <div className="flex-1">
                      <div className="font-semibold text-sm">{currentOrg.name}</div>
                      {testMode && (
                        <div className="mt-1">
                          <span className="inline-flex items-center px-2 py-1 rounded text-xs font-medium bg-orange-100 text-orange-800">
                            Test mode
                          </span>
                        </div>
                      )}
                    </div>
                  </div>
                </div>

                {/* Settings */}
                <div className="p-3 border-b">
                  <AppLink
                    href="/settings"
                    className="w-full flex items-center gap-3 px-3 py-2 text-sm text-left rounded-md hover:bg-muted transition-colors"
                    onClick={() => setOpen(false)}
                  >
                    <Settings className="size-4 text-muted-foreground" />
                    <span>Settings</span>
                  </AppLink>
                </div>

                {/* Organizations */}
                {organizations!.length > 1 && (
                  <div className="p-3 border-b">
                    <div className="text-xs font-medium text-muted-foreground mb-2 px-3">Switch to</div>

                    {organizations!.filter(org => org.id !== currentOrg.id).map((org, index) => (
                      <button
                        key={`org-${org.id}`}
                        onClick={() => select(org)()}
                        className="w-full flex items-center gap-3 px-3 py-2 text-sm text-left rounded-md hover:bg-muted transition-colors"
                      >
                        <div className="flex size-6 items-center justify-center rounded border text-xs font-medium bg-muted text-muted-foreground">
                          {org.name.charAt(0).toUpperCase()}
                        </div>
                        <span className="flex-1 truncate">{org.name}</span>
                      </button>
                    ))}

                    {/* Create organization */}
                    {ALLOW_MULTI_ACCOUNT && (
                      <button
                        onClick={create}
                        className="w-full flex items-center gap-3 px-3 py-2 text-sm text-left rounded-md hover:bg-muted transition-colors mt-2"
                      >
                        <Plus className="size-4 text-muted-foreground" />
                        <span>Create account</span>
                      </button>
                    )}
                  </div>
                )}

                {/* User Section */}
                <div className="p-3">
                  <AppLink
                    href="/settings/profile"
                    className="w-full flex items-center gap-3 px-3 py-2 text-sm text-left rounded-md hover:bg-muted transition-colors"
                    onClick={() => setOpen(false)}
                  >
                    <User className="size-4 text-muted-foreground" />
                    <span>{user?.full_name || user?.email || "Profile"}</span>
                  </AppLink>
                  <button
                    onClick={() => {
                      setOpen(false);
                      signOut({ callbackUrl: "/" });
                    }}
                    className="w-full flex items-center gap-3 px-3 py-2 text-sm text-left rounded-md hover:bg-muted transition-colors text-red-600 hover:text-red-700"
                  >
                    <LogOut className="size-4" />
                    <span>Sign out</span>
                  </button>
                </div>
              </div>
            </PopoverContent>
          </Popover>
        </SidebarMenuItem>
      </SidebarMenu>
    );
  }

  // Final fallback - show placeholder animation
  return renderPlaceholder();
}
