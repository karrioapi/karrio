"use client";

import { useState } from "react";
import { Dialog, DialogContent, DialogHeader, DialogTitle } from "./ui/dialog";
import { Button } from "./ui/button";
import { Badge } from "./ui/badge";
import { Avatar, AvatarFallback } from "./ui/avatar";
import { Label } from "./ui/label";
import { RadioGroup, RadioGroupItem } from "./ui/radio-group";
import { User, Shield, Eye } from "lucide-react";

interface TeamMember {
  email: string;
  full_name?: string | null;
  is_admin: boolean;
  is_owner: boolean | null;
  user_id?: string | null;
}

interface RoleManagementDialogProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  member: TeamMember | null;
  onUpdateRole: (userId: string, roles: string[]) => void;
  isLoading?: boolean;
}

export function RoleManagementDialog({
  open,
  onOpenChange,
  member,
  onUpdateRole,
  isLoading = false
}: RoleManagementDialogProps) {
  const [selectedRole, setSelectedRole] = useState<string>("member");

  const getInitials = (name?: string | null, email?: string) => {
    if (name) {
      return name.split(' ').map(n => n[0]).join('').toUpperCase().slice(0, 2);
    }
    if (email) {
      return email.slice(0, 2).toUpperCase();
    }
    return 'U';
  };

  const getCurrentRole = () => {
    if (!member) return "member";
    if (member.is_owner) return "owner";
    if (member.is_admin) return "admin";
    return "member";
  };

  const handleOpenChange = (newOpen: boolean) => {
    if (newOpen && member) {
      setSelectedRole(getCurrentRole());
    }
    onOpenChange(newOpen);
  };

  const handleSave = () => {
    if (member) {
      // Use user_id if available, otherwise use email as identifier
      const userId = member.user_id || member.email;
      const roles = [];
      if (selectedRole === "admin") {
        roles.push("admin");
      }
      // Note: We don't handle owner role changes here as that's usually a separate operation
      onUpdateRole(userId, roles);
      onOpenChange(false);
    }
  };

  if (!member) return null;

  const currentRole = getCurrentRole();
  const isOwner = member.is_owner;

  return (
    <Dialog open={open} onOpenChange={handleOpenChange}>
      <DialogContent className="sm:max-w-md p-4 pb-8">
        <DialogHeader>
          <DialogTitle>Manage Role</DialogTitle>
        </DialogHeader>

        <div className="space-y-6">
          {/* Member Info */}
          <div className="flex items-center space-x-3">
            <Avatar className="h-10 w-10">
              <AvatarFallback>
                {getInitials(member.full_name, member.email)}
              </AvatarFallback>
            </Avatar>
            <div>
              <div className="font-medium">
                {member.full_name || member.email}
              </div>
              <div className="text-sm text-muted-foreground">
                {member.email}
              </div>
            </div>
          </div>

          {/* Current Role */}
          <div className="space-y-2">
            <Label className="text-sm font-medium">Current Role</Label>
            <div className="flex items-center space-x-2">
              {isOwner && (
                <Badge variant="default" className="text-xs">
                  Owner
                </Badge>
              )}
              {member.is_admin && (
                <Badge variant="secondary" className="text-xs">
                  Admin
                </Badge>
              )}
              {!member.is_admin && !isOwner && (
                <Badge variant="outline" className="text-xs">
                  Member
                </Badge>
              )}
            </div>
          </div>

          {/* Role Selection */}
          {!isOwner && (
            <div className="space-y-4">
              <Label className="text-sm font-medium">Change Role</Label>
              <RadioGroup value={selectedRole} onValueChange={setSelectedRole}>
                <div className="flex items-center space-x-3 p-3 border rounded-lg">
                  <RadioGroupItem value="member" id="member" />
                  <div className="flex items-center space-x-2 flex-1">
                    <Eye className="h-4 w-4 text-muted-foreground" />
                    <div>
                      <Label htmlFor="member" className="font-medium cursor-pointer">
                        Member
                      </Label>
                      <p className="text-sm text-muted-foreground">
                        Can view organization data and resources
                      </p>
                    </div>
                  </div>
                </div>

                <div className="flex items-center space-x-3 p-3 border rounded-lg">
                  <RadioGroupItem value="admin" id="admin" />
                  <div className="flex items-center space-x-2 flex-1">
                    <Shield className="h-4 w-4 text-muted-foreground" />
                    <div>
                      <Label htmlFor="admin" className="font-medium cursor-pointer">
                        Admin
                      </Label>
                      <p className="text-sm text-muted-foreground">
                        Can manage team members and organization settings
                      </p>
                    </div>
                  </div>
                </div>
              </RadioGroup>
            </div>
          )}

          {isOwner && (
            <div className="p-3 bg-muted rounded-lg">
              <p className="text-sm text-muted-foreground">
                The organization owner role cannot be changed from this dialog.
                Use the "Change Owner" feature to transfer ownership.
              </p>
            </div>
          )}

          {/* Actions */}
          <div className="flex justify-end space-x-2">
            <Button variant="outline" onClick={() => onOpenChange(false)}>
              Cancel
            </Button>
            {!isOwner && (
              <Button
                onClick={handleSave}
                disabled={isLoading || selectedRole === currentRole}
              >
                {isLoading ? "Updating..." : "Update Role"}
              </Button>
            )}
          </div>
        </div>
      </DialogContent>
    </Dialog>
  );
}
