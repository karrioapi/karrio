"use client";

import React, { useState, useEffect } from "react";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@karrio/ui/components/ui/dialog";
import { Button } from "@karrio/ui/components/ui/button";
import { Input } from "@karrio/ui/components/ui/input";
import { Label } from "@karrio/ui/components/ui/label";
import { Checkbox } from "@karrio/ui/components/ui/checkbox";
import {
  GetUsers_users_edges_node as User,
  GetPermissionGroups_permission_groups_edges_node as PermissionGroup,
} from "@karrio/types/graphql/admin/types";

interface StaffEditModalProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  onSubmit: (e: React.FormEvent<HTMLFormElement>) => void;
  user: User | null;
  permissionGroups: PermissionGroup[];
  isLoading: boolean;
}

export function StaffEditModal({
  open,
  onOpenChange,
  onSubmit,
  user,
  permissionGroups,
  isLoading,
}: StaffEditModalProps) {
  const [selectedGroups, setSelectedGroups] = useState<Set<string>>(new Set());

  // Initialize selected groups when user changes or modal opens
  useEffect(() => {
    if (user?.permissions) {
      setSelectedGroups(new Set(user.permissions));
    } else {
      setSelectedGroups(new Set());
    }
  }, [user, open]);

  const handleGroupToggle = (groupId: string, checked: boolean) => {
    const newSelected = new Set(selectedGroups);
    if (checked) {
      newSelected.add(groupId);
    } else {
      newSelected.delete(groupId);
    }
    setSelectedGroups(newSelected);
  };

  const handleSelectAll = () => {
    if (selectedGroups.size === permissionGroups.length) {
      // If all are selected, deselect all
      setSelectedGroups(new Set());
    } else {
      // Select all groups
      setSelectedGroups(new Set(permissionGroups.map(g => String(g.id))));
    }
  };

  const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    // Add selected groups to form data
    const form = e.currentTarget;
    // Remove existing permission_groups checkboxes
    const existingCheckboxes = form.querySelectorAll('input[name="permission_groups"]');
    existingCheckboxes.forEach(cb => {
      (cb as HTMLInputElement).checked = selectedGroups.has((cb as HTMLInputElement).value);
    });
    onSubmit(e);
  };
  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="max-w-2xl max-h-[90vh] p-0 flex flex-col">
        {/* Sticky Header */}
        <DialogHeader className="px-4 py-3 border-b sticky top-0 bg-background z-10">
          <DialogTitle>
            Edit Staff Member
          </DialogTitle>
          <DialogDescription>
            Update user details, permissions, and access levels for {user?.full_name || user?.email}.
          </DialogDescription>
        </DialogHeader>

        <form onSubmit={handleSubmit} className="flex flex-col flex-1 min-h-0">
          {/* Scrollable Body */}
          <div className="flex-1 overflow-y-auto px-4 py-3">
            <div className="space-y-6">
              {/* Personal Information */}
              <div className="space-y-4">
                <h3 className="text-lg font-semibold">Personal Information</h3>
                <div className="grid gap-4">
                  <div className="space-y-2">
                    <Label htmlFor="edit_full_name">Full Name</Label>
                    <Input
                      id="edit_full_name"
                      name="full_name"
                      defaultValue={user?.full_name || ""}
                      placeholder="Enter full name"
                      required
                    />
                  </div>
                  <div className="space-y-2">
                    <Label>Email Address</Label>
                    <Input
                      value={user?.email || ""}
                      disabled
                      className="bg-muted"
                    />
                    <p className="text-xs text-muted-foreground">
                      Email addresses cannot be changed for security reasons
                    </p>
                  </div>
                </div>
              </div>

              {/* Account Status */}
              <div className="space-y-4">
                <h3 className="text-lg font-semibold">Account Status</h3>
                <div className="space-y-4">
                  <div className="flex items-center space-x-3 p-4 rounded-lg border">
                    <Checkbox
                      id="edit_is_active"
                      name="is_active"
                      defaultChecked={user?.is_active}
                    />
                    <div className="space-y-1">
                      <Label htmlFor="edit_is_active" className="text-sm font-medium">
                        Active Account
                      </Label>
                      <p className="text-xs text-muted-foreground">
                        User can sign in and access the platform
                      </p>
                    </div>
                  </div>
                </div>
              </div>

              {/* Role & Permissions */}
              <div className="space-y-4">
                <h3 className="text-lg font-semibold">Role & Permissions</h3>
                <div className="space-y-4">
                  <div className="flex items-center space-x-3 p-4 rounded-lg border">
                    <Checkbox
                      id="edit_is_staff"
                      name="is_staff"
                      defaultChecked={user?.is_staff}
                    />
                    <div className="space-y-1">
                      <Label htmlFor="edit_is_staff" className="text-sm font-medium">
                        Administrator Access
                      </Label>
                      <p className="text-xs text-muted-foreground">
                        Full access to admin console and system management
                      </p>
                    </div>
                  </div>

                  {permissionGroups.length > 0 && (
                    <div className="space-y-3">
                      <div className="flex items-center justify-between">
                        <Label className="text-sm font-medium">Permission Groups</Label>
                        <Button
                          type="button"
                          variant="ghost"
                          size="sm"
                          onClick={handleSelectAll}
                          className="h-auto py-1 px-2 text-xs"
                        >
                          {selectedGroups.size === permissionGroups.length ? "Deselect All" : "Select All"}
                        </Button>
                      </div>
                      <div className="space-y-2 max-h-32 overflow-y-auto border rounded-lg p-3">
                        {permissionGroups.map((group) => (
                          <div key={group.id} className="flex items-center space-x-3">
                            <Checkbox
                              id={`edit_permission_${group.id}`}
                              name="permission_groups"
                              value={String(group.id)}
                              checked={selectedGroups.has(String(group.id))}
                              onCheckedChange={(checked) => handleGroupToggle(String(group.id), !!checked)}
                            />
                            <Label 
                              htmlFor={`edit_permission_${group.id}`}
                              className="text-sm cursor-pointer"
                            >
                              {group.name}
                            </Label>
                          </div>
                        ))}
                      </div>
                      <p className="text-xs text-muted-foreground">
                        Select specific permission groups for granular access control
                      </p>
                    </div>
                  )}
                </div>
              </div>
            </div>
          </div>

          {/* Sticky Footer */}
          <DialogFooter className="px-4 py-3 border-t sticky bottom-0 bg-background">
            <Button
              type="button"
              variant="outline"
              onClick={() => onOpenChange(false)}
            >
              Cancel
            </Button>
            <Button type="submit" disabled={isLoading}>
              {isLoading ? (
                <>
                  <div className="h-4 w-4 animate-spin rounded-full border-2 border-current border-t-transparent mr-2" />
                  Updating...
                </>
              ) : (
                "Update User"
              )}
            </Button>
          </DialogFooter>
        </form>
      </DialogContent>
    </Dialog>
  );
}