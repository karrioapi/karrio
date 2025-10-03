"use client";

import { useState } from "react";
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
import { Switch } from "@karrio/ui/components/ui/switch";
import {
  GetPermissionGroups_permission_groups_edges_node as PermissionGroup,
} from "@karrio/types/graphql/admin/types";

interface StaffInviteModalProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  onSubmit: (data: any) => void;
  isLoading: boolean;
  permissionGroups?: PermissionGroup[];
}

export function StaffInviteModal({
  open,
  onOpenChange,
  onSubmit,
  isLoading,
  permissionGroups = [],
}: StaffInviteModalProps) {
  const [formData, setFormData] = useState({
    full_name: "",
    email: "",
    password1: "",
    password2: "",
    is_staff: false,
    is_active: true,
    is_superuser: false,
    permissions: [] as string[],
  });

  const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    onSubmit(formData);
  };

  const handlePermissionChange = (groupName: string, checked: boolean) => {
    setFormData(prev => ({
      ...prev,
      permissions: checked
        ? [...prev.permissions, groupName]
        : prev.permissions.filter(p => p !== groupName)
    }));
  };

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="max-w-lg max-h-[90vh] p-0 flex flex-col">
        {/* Sticky Header */}
        <DialogHeader className="px-4 py-3 border-b sticky top-0 bg-background z-10">
          <DialogTitle>
            Add User
          </DialogTitle>
          <DialogDescription>
            Add a user to your team with specific roles and permissions. If the user already exists, their permissions will be updated.
          </DialogDescription>
        </DialogHeader>

        <form onSubmit={handleSubmit} className="flex flex-col flex-1 min-h-0">
          {/* Scrollable Body */}
          <div className="flex-1 overflow-y-auto px-4 py-3">
            <div className="space-y-4">
              {/* Basic Information */}
              <div className="space-y-4">
                <h3 className="text-sm font-medium">Basic Information</h3>
                <div className="space-y-2">
                  <Label htmlFor="invite_full_name">Full Name</Label>
                  <Input
                    id="invite_full_name"
                    value={formData.full_name}
                    onChange={(e) => setFormData(prev => ({ ...prev, full_name: e.target.value }))}
                    placeholder="Enter full name"
                    required
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="invite_email">Email Address</Label>
                  <Input
                    id="invite_email"
                    type="email"
                    value={formData.email}
                    onChange={(e) => setFormData(prev => ({ ...prev, email: e.target.value }))}
                    placeholder="user@example.com"
                    required
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="invite_password1">Password</Label>
                  <Input
                    id="invite_password1"
                    type="password"
                    value={formData.password1}
                    onChange={(e) => setFormData(prev => ({ ...prev, password1: e.target.value }))}
                    placeholder="Enter password"
                    required
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="invite_password2">Confirm Password</Label>
                  <Input
                    id="invite_password2"
                    type="password"
                    value={formData.password2}
                    onChange={(e) => setFormData(prev => ({ ...prev, password2: e.target.value }))}
                    placeholder="Confirm password"
                    required
                  />
                </div>
              </div>

              {/* Account Status */}
              <div className="space-y-4">
                <h3 className="text-sm font-medium">Account Status</h3>
                <div className="space-y-3">
                  <div className="flex items-center justify-between">
                    <Label htmlFor="is_active" className="flex flex-col">
                      <span>Active Account</span>
                      <span className="text-xs text-muted-foreground font-normal">User can log in immediately</span>
                    </Label>
                    <Switch
                      id="is_active"
                      checked={formData.is_active}
                      onCheckedChange={(checked) => setFormData(prev => ({ ...prev, is_active: checked }))}
                    />
                  </div>
                  <div className="flex items-center justify-between">
                    <Label htmlFor="is_staff" className="flex flex-col">
                      <span>Staff Status</span>
                      <span className="text-xs text-muted-foreground font-normal">Can access admin interface</span>
                    </Label>
                    <Switch
                      id="is_staff"
                      checked={formData.is_staff}
                      onCheckedChange={(checked) => setFormData(prev => ({ ...prev, is_staff: checked }))}
                    />
                  </div>
                  <div className="flex items-center justify-between">
                    <Label htmlFor="is_superuser" className="flex flex-col">
                      <span>Superuser Status</span>
                      <span className="text-xs text-muted-foreground font-normal">Has all permissions without explicit assignment</span>
                    </Label>
                    <Switch
                      id="is_superuser"
                      checked={formData.is_superuser}
                      onCheckedChange={(checked) => setFormData(prev => ({ ...prev, is_superuser: checked }))}
                    />
                  </div>
                </div>
              </div>

              {/* Permissions */}
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
                            id={`perm_${group.id}`}
                            checked={formData.permissions.includes(group.name)}
                            onCheckedChange={(checked) => handlePermissionChange(group.name, checked as boolean)}
                            disabled={formData.is_superuser}
                          />
                          <Label
                            htmlFor={`perm_${group.id}`}
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
                  Adding...
                </>
              ) : (
                "Add User"
              )}
            </Button>
          </DialogFooter>
        </form>
      </DialogContent>
    </Dialog>
  );
}
