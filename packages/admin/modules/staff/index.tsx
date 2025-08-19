"use client";

import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
} from "@karrio/ui/components/ui/card";
import { Button } from "@karrio/ui/components/ui/button";
import { useToast } from "@karrio/ui/hooks/use-toast";
import { useState } from "react";
import { useUsers, useUserMutation, usePermissionGroups } from "@karrio/hooks/admin-users";
import {
  GetUsers_users_edges_node as User,
} from "@karrio/types/graphql/admin/types";
import { ConfirmationDialog } from "@karrio/ui/components/confirmation-dialog";

// Import our extracted components
import { StaffInviteModal } from "@karrio/admin/components/staff-invite-modal";
import { StaffEditModal } from "@karrio/admin/components/staff-edit-modal";
import { StaffTable } from "@karrio/admin/components/staff-table";
import { StaffEmptyState } from "@karrio/admin/components/staff-empty-state";
import { PermissionsTable } from "@karrio/admin/components/permissions-table";
import { cn } from "@karrio/ui/lib/utils";

export default function Page() {
  const { toast } = useToast();
  const [selectedTab, setSelectedTab] = useState("staff");
  const [isInviteOpen, setIsInviteOpen] = useState(false);
  const [isEditOpen, setIsEditOpen] = useState(false);
  const [selectedUser, setSelectedUser] = useState<User | null>(null);
  const [cursor, setCursor] = useState<string | undefined>(undefined);

  // Additional modals and confirmation states
  const [isResetPasswordOpen, setIsResetPasswordOpen] = useState(false);
  const [isDisableConfirmOpen, setIsDisableConfirmOpen] = useState(false);
  const [isResendInviteOpen, setIsResendInviteOpen] = useState(false);
  const [pendingActionUser, setPendingActionUser] = useState<User | null>(null);

  // Fetch users and permission groups
  const { query: usersQuery, users: usersData } = useUsers({
    is_active: true,
  });
  const { query: permissionGroupsQuery, permission_groups: permissionGroupsData } = usePermissionGroups();
  const users = usersData?.edges || [];
  const permissionGroups = permissionGroupsData?.edges || [];
  const isLoadingUsers = usersQuery.isLoading;
  const isLoadingPermissions = permissionGroupsQuery.isLoading;

  // Mutations
  const { createUser, updateUser, removeUser } = useUserMutation();

  const handleCreateSuccess = () => {
    toast({ title: "User created successfully" });
    setIsInviteOpen(false);
  };

  const handleUpdateSuccess = () => {
    toast({ title: "User updated successfully" });
    setIsEditOpen(false);
  };

  const handleRemoveSuccess = () => {
    toast({ title: "User removed successfully" });
  };

  const handleError = (error: any, action: string) => {
    toast({
      title: `Failed to ${action} user`,
      description: error.message || "An error occurred",
      variant: "destructive",
    });
  };

  const handleInvite = async (data: any) => {
    createUser.mutate(
      {
        email: data.email,
        full_name: data.full_name,
        password1: data.password1,
        password2: data.password2,
        is_staff: data.is_staff,
        is_active: data.is_active,
        is_superuser: data.is_superuser,
        permissions: data.permissions,
      },
      {
        onSuccess: (response) => {
          // Check if user already existed by looking for typical creation vs update indicators
          toast({
            title: "User added successfully",
            description: "User has been configured with the specified permissions and access level."
          });
          setIsInviteOpen(false);
        },
        onError: (error) => handleError(error, "add"),
      },
    );
  };

  const handleUpdate = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const formData = new FormData(e.currentTarget);
    const permissions = Array.from(
      formData.getAll("permission_groups"),
    ) as string[];

    if (!selectedUser) return;

    updateUser.mutate(
      {
        id: selectedUser.id as any,
        full_name: formData.get("full_name") as string,
        is_staff: formData.get("is_staff") === "on",
        is_active: formData.get("is_active") === "on",
        is_superuser: formData.get("is_superuser") === "on",
        permissions,
      },
      {
        onSuccess: handleUpdateSuccess,
        onError: (error) => handleError(error, "update"),
      },
    );
  };

  // Remove user confirmation
  const [confirmOpen, setConfirmOpen] = useState(false);
  const [pendingUser, setPendingUser] = useState<User | null>(null);
  const askRemove = (user: User) => { setPendingUser(user); setConfirmOpen(true); };
  const handleRemoveConfirmed = () => {
    if (!pendingUser) return;
    removeUser.mutate(
      { id: pendingUser.id as any },
      { onSuccess: handleRemoveSuccess, onError: (error) => handleError(error, "remove") },
    );
    setPendingUser(null);
  };


  const handleToggleAccountStatus = (user: User) => {
    const newStatus = !user.is_active;
    updateUser.mutate(
      {
        id: user.id as any,
        is_active: newStatus,
      },
      {
        onSuccess: () => {
          toast({
            title: `Account ${newStatus ? 'enabled' : 'disabled'}`,
            description: `${user.full_name || user.email} has been ${newStatus ? 'enabled' : 'disabled'}`,
          });
        },
        onError: (error) => handleError(error, newStatus ? "enable" : "disable"),
      },
    );
  };

  // Fix mutation status checks
  const isInviting = createUser.isLoading;
  const isUpdating = updateUser.isLoading;
  const isRemoving = removeUser.isLoading;

  if (isLoadingUsers || isLoadingPermissions) {
    return (
      <div className="flex h-[calc(100vh-4rem)] items-center justify-center">
        <div className="h-8 w-8 animate-spin rounded-full border-4 border-primary border-t-transparent"></div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Staff & Permissions</h1>
          <p className="text-muted-foreground">
            Manage your team members and their access permissions
          </p>
        </div>
        {selectedTab === "staff" && (
          <Button onClick={() => setIsInviteOpen(true)}>
            Add User
          </Button>
        )}
      </div>

      {/* Tab Navigation */}
      <div className="border-b">
        <nav className="flex space-x-8">
          <button
            className={cn(
              "whitespace-nowrap border-b-2 py-4 px-1 text-sm font-medium transition-colors",
              selectedTab === "staff"
                ? "border-purple-500 text-purple-600"
                : "border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300"
            )}
            onClick={() => setSelectedTab("staff")}
          >
            Staff Members
          </button>
          <button
            className={cn(
              "whitespace-nowrap border-b-2 py-4 px-1 text-sm font-medium transition-colors",
              selectedTab === "permissions"
                ? "border-purple-500 text-purple-600"
                : "border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300"
            )}
            onClick={() => setSelectedTab("permissions")}
          >
            Permissions & Groups
          </button>
        </nav>
      </div>

      {/* Content */}
      <div className="mt-6">
        {selectedTab === "staff" && (
          <Card>
            <CardHeader>
              <CardTitle>
                Team Members ({users.length})
              </CardTitle>
            </CardHeader>
            <CardContent>
              {users.length === 0 ? (
                <StaffEmptyState onInvite={() => setIsInviteOpen(true)} />
              ) : (
                <>
                  <StaffTable
                    users={users}
                    onEdit={(user) => {
                      setSelectedUser(user);
                      setIsEditOpen(true);
                    }}
                    onToggleStatus={handleToggleAccountStatus}
                    onRemove={askRemove}
                  />

                  {usersData?.page_info && (
                    <div className="mt-4 flex items-center justify-between">
                      <p className="text-sm text-muted-foreground">
                        Showing {users.length} of {usersData.page_info.count} users
                      </p>
                      <div className="flex items-center space-x-2">
                        <Button
                          variant="outline"
                          size="sm"
                          onClick={() => setCursor(usersData.page_info.start_cursor || undefined)}
                          disabled={!usersData.page_info.has_previous_page}
                        >
                          Previous
                        </Button>
                        <Button
                          variant="outline"
                          size="sm"
                          onClick={() => setCursor(usersData.page_info.end_cursor || undefined)}
                          disabled={!usersData.page_info.has_next_page}
                        >
                          Next
                        </Button>
                      </div>
                    </div>
                  )}
                </>
              )}
            </CardContent>
          </Card>
        )}

        {selectedTab === "permissions" && (
          <PermissionsTable
            permissionGroups={permissionGroups}
            isLoading={isLoadingPermissions}
          />
        )}
      </div>

      {/* Confirmation dialogs */}
      <ConfirmationDialog
        open={confirmOpen}
        onOpenChange={setConfirmOpen}
        title="Remove User"
        description={`Are you sure you want to remove ${(pendingUser as any)?.full_name || 'this user'}? This action cannot be undone.`}
        confirmLabel="Remove"
        onConfirm={handleRemoveConfirmed}
      />

      {/* Modals */}
      <StaffInviteModal
        open={isInviteOpen}
        onOpenChange={setIsInviteOpen}
        onSubmit={handleInvite}
        isLoading={isInviting}
        permissionGroups={permissionGroups.map(({ node }) => node) as any}
      />

      <StaffEditModal
        open={isEditOpen}
        onOpenChange={setIsEditOpen}
        onSubmit={handleUpdate}
        user={selectedUser}
        permissionGroups={permissionGroups.map(({ node }) => node)}
        isLoading={isUpdating}
      />
    </div>
  );
}
