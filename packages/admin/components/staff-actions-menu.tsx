"use client";

import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@karrio/ui/components/ui/dropdown-menu";
import { Button } from "@karrio/ui/components/ui/button";
import { MoreHorizontal } from "lucide-react";
import {
  GetUsers_users_edges_node as User,
} from "@karrio/types/graphql/admin/types";

interface StaffActionsMenuProps {
  user: User;
  onEdit: (user: User) => void;
  onResetPassword: (user: User) => void;
  onResendInvitation: (user: User) => void;
  onToggleStatus: (user: User) => void;
  onRemove: (user: User) => void;
}

export function StaffActionsMenu({
  user,
  onEdit,
  onResetPassword,
  onResendInvitation,
  onToggleStatus,
  onRemove,
}: StaffActionsMenuProps) {
  return (
    <DropdownMenu>
      <DropdownMenuTrigger asChild>
        <Button
          variant="ghost"
          size="icon"
          className="h-8 w-8 p-0 hover:bg-muted"
        >
          <MoreHorizontal className="h-4 w-4" />
          <span className="sr-only">Open menu</span>
        </Button>
      </DropdownMenuTrigger>
      <DropdownMenuContent align="end" className="w-56">
        <DropdownMenuItem onClick={() => onEdit(user)}>
          <span>Edit Details</span>
        </DropdownMenuItem>
        {user.last_login ? (
          <DropdownMenuItem onClick={() => onResetPassword(user)}>
            <span>Reset Password</span>
          </DropdownMenuItem>
        ) : (
          <DropdownMenuItem onClick={() => onResendInvitation(user)}>
            <span>Resend Invitation</span>
          </DropdownMenuItem>
        )}
        <DropdownMenuSeparator />
        <DropdownMenuItem onClick={() => onToggleStatus(user)}>
          <span>{user.is_active ? "Disable Account" : "Enable Account"}</span>
        </DropdownMenuItem>
        <DropdownMenuSeparator />
        <DropdownMenuItem
          className="text-destructive focus:text-destructive"
          onClick={() => onRemove(user)}
        >
          <span>Remove User</span>
        </DropdownMenuItem>
      </DropdownMenuContent>
    </DropdownMenu>
  );
}