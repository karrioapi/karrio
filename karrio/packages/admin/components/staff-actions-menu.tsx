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
import { useUser } from "@karrio/hooks/user";

interface StaffActionsMenuProps {
  user: User;
  onEdit: (user: User) => void;
  onToggleStatus: (user: User) => void;
  onRemove: (user: User) => void;
}

export function StaffActionsMenu({
  user,
  onEdit,
  onToggleStatus,
  onRemove,
}: StaffActionsMenuProps) {
  const { query: userQuery } = useUser();
  const currentUser = userQuery.data?.user;
  
  // Check if this is the current user
  const isCurrentUser = currentUser?.email === user.email;
  
  // Don't show menu for current user
  if (isCurrentUser) {
    return null;
  }

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
