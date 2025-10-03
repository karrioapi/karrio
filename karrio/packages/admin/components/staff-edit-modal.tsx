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
import { Switch } from "@karrio/ui/components/ui/switch";
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
  const [formData, setFormData] = useState({
    full_name: "",
    is_active: true,
    is_staff: false,
    is_superuser: false,
    permissions: [] as string[],
  });

  // Initialize form data when user changes or modal opens
  useEffect(() => {
    if (user) {
      setFormData({
        full_name: user.full_name || "",
        is_active: user.is_active ?? true,
        is_staff: user.is_staff ?? false,
        is_superuser: user.is_superuser ?? false,
        permissions: user.permissions || [],
      });
    }
  }, [user, open]);

  const handlePermissionChange = (groupName: string, checked: boolean) => {
    setFormData(prev => ({
      ...prev,
      permissions: checked 
        ? [...prev.permissions, groupName]
        : prev.permissions.filter(p => p !== groupName)
    }));
  };

  const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const form = e.currentTarget;
    
    // Create hidden inputs for the form data
    Object.entries(formData).forEach(([key, value]) => {
      if (key === 'permissions') {
        // Handle permissions array
        (value as string[]).forEach(permission => {
          const input = document.createElement('input');
          input.type = 'hidden';
          input.name = 'permission_groups';
          input.value = permission;
          form.appendChild(input);
        });
      } else if (typeof value === 'boolean') {
        // Handle boolean values
        const input = document.createElement('input');
        input.type = 'hidden';
        input.name = key;
        input.value = value ? 'on' : '';
        form.appendChild(input);
      } else {
        // Handle string values
        const existingInput = form.querySelector(`input[name="${key}"]`);
        if (!existingInput) {
          const input = document.createElement('input');
          input.type = 'hidden';
          input.name = key;
          input.value = value as string;
          form.appendChild(input);
        }
      }
    });
    
    onSubmit(e);
  };

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="max-w-lg max-h-[90vh] p-0 flex flex-col">
        {/* Sticky Header */}
        <DialogHeader className="px-4 py-3 border-b sticky top-0 bg-background z-10">
          <DialogTitle>
            Edit User
          </DialogTitle>
          <DialogDescription>
            Update user details and permissions for {user?.email}
          </DialogDescription>
        </DialogHeader>

        <form onSubmit={handleSubmit} className="flex flex-col flex-1 min-h-0">
          {/* Scrollable Body */}
          <div className="flex-1 overflow-y-auto px-4 py-3">
            <div className="space-y-4">
              {/* Basic Information */}
              <div className="space-y-3">
                <div className="space-y-2">
                  <Label htmlFor="edit_full_name">Full Name</Label>
                  <Input
                    id="edit_full_name"
                    name="full_name"
                    value={formData.full_name}
                    onChange={(e) => setFormData(prev => ({ ...prev, full_name: e.target.value }))}
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
                </div>
              </div>

              {/* Account Status - Compact switches */}
              <div className="space-y-3">
                <h3 className="text-sm font-medium">Account Settings</h3>
                <div className="space-y-2">
                  <div className="flex items-center justify-between py-1">
                    <Label htmlFor="edit_is_active" className="flex flex-col cursor-pointer">
                      <span className="text-sm">Active Account</span>
                      <span className="text-xs text-muted-foreground font-normal">User can log in</span>
                    </Label>
                    <Switch
                      id="edit_is_active"
                      checked={formData.is_active}
                      onCheckedChange={(checked) => setFormData(prev => ({ ...prev, is_active: checked }))}
                    />
                  </div>
                  <div className="flex items-center justify-between py-1">
                    <Label htmlFor="edit_is_staff" className="flex flex-col cursor-pointer">
                      <span className="text-sm">Staff Status</span>
                      <span className="text-xs text-muted-foreground font-normal">Access admin interface</span>
                    </Label>
                    <Switch
                      id="edit_is_staff"
                      checked={formData.is_staff}
                      onCheckedChange={(checked) => setFormData(prev => ({ ...prev, is_staff: checked }))}
                    />
                  </div>
                  <div className="flex items-center justify-between py-1">
                    <Label htmlFor="edit_is_superuser" className="flex flex-col cursor-pointer">
                      <span className="text-sm">Superuser</span>
                      <span className="text-xs text-muted-foreground font-normal">All permissions</span>
                    </Label>
                    <Switch
                      id="edit_is_superuser"
                      checked={formData.is_superuser}
                      onCheckedChange={(checked) => setFormData(prev => ({ ...prev, is_superuser: checked }))}
                    />
                  </div>
                </div>
              </div>

              {/* Permission Groups - Only show if not superuser */}
              {permissionGroups.length > 0 && !formData.is_superuser && (
                <div className="space-y-3">
                  <div className="flex items-center justify-between">
                    <h3 className="text-sm font-medium">Permission Groups</h3>
                    <button
                      type="button"
                      onClick={() => {
                        if (formData.permissions.length === permissionGroups.length) {
                          setFormData(prev => ({ ...prev, permissions: [] }));
                        } else {
                          setFormData(prev => ({ 
                            ...prev, 
                            permissions: permissionGroups.map(g => g.name) 
                          }));
                        }
                      }}
                      className="text-xs text-primary hover:underline"
                    >
                      {formData.permissions.length === permissionGroups.length ? 'Clear All' : 'Select All'}
                    </button>
                  </div>
                  <div className="border rounded-md">
                    <div className="max-h-40 overflow-y-auto p-3 space-y-2">
                      {permissionGroups.map((group) => (
                        <div key={group.id} className="flex items-center space-x-2 hover:bg-muted/50 rounded px-1 py-0.5">
                          <Checkbox
                            id={`edit_perm_${group.id}`}
                            checked={formData.permissions.includes(group.name)}
                            onCheckedChange={(checked) => handlePermissionChange(group.name, checked as boolean)}
                            disabled={formData.is_superuser}
                          />
                          <Label
                            htmlFor={`edit_perm_${group.id}`}
                            className="text-sm font-normal cursor-pointer flex-1 py-1"
                          >
                            {group.name}
                          </Label>
                        </div>
                      ))}
                    </div>
                    {formData.permissions.length > 0 && (
                      <div className="px-3 py-2 bg-muted/50 border-t text-xs text-muted-foreground">
                        {formData.permissions.length} of {permissionGroups.length} selected
                      </div>
                    )}
                  </div>
                </div>
              )}

              {/* User Metadata */}
              {user && (
                <div className="pt-2 border-t">
                  <div className="grid grid-cols-2 gap-2 text-xs text-muted-foreground">
                    <div>
                      <span className="font-medium">Created:</span> {new Date(user.date_joined).toLocaleDateString()}
                    </div>
                    {user.last_login && (
                      <div>
                        <span className="font-medium">Last login:</span> {new Date(user.last_login).toLocaleDateString()}
                      </div>
                    )}
                  </div>
                </div>
              )}
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
                "Save Changes"
              )}
            </Button>
          </DialogFooter>
        </form>
      </DialogContent>
    </Dialog>
  );
}