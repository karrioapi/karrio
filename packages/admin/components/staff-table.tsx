"use client";

import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@karrio/ui/components/ui/table";
import { Badge } from "@karrio/ui/components/ui/badge";
import { format } from "date-fns";
import {
  GetUsers_users_edges_node as User,
} from "@karrio/types/graphql/admin/types";
import { StaffActionsMenu } from "./staff-actions-menu";

interface StaffTableProps {
  users: Array<{ node: User }>;
  onEdit: (user: User) => void;
  onResetPassword: (user: User) => void;
  onResendInvitation: (user: User) => void;
  onToggleStatus: (user: User) => void;
  onRemove: (user: User) => void;
}

export function StaffTable({
  users,
  onEdit,
  onResetPassword,
  onResendInvitation,
  onToggleStatus,
  onRemove,
}: StaffTableProps) {
  return (
    <Table>
      <TableHeader>
        <TableRow>
          <TableHead>Member</TableHead>
          <TableHead>Role</TableHead>
          <TableHead>Status</TableHead>
          <TableHead>Last Login</TableHead>
          <TableHead className="w-[50px]">Actions</TableHead>
        </TableRow>
      </TableHeader>
      <TableBody>
        {users.map(({ node: user }) => (
          <TableRow key={user.id}>
            <TableCell>
              <div className="flex items-center gap-3">
                <div className="flex h-8 w-8 items-center justify-center rounded-full bg-primary/10">
                  <span className="text-sm font-medium">
                    {user.full_name?.charAt(0)?.toUpperCase() || user.email.charAt(0).toUpperCase()}
                  </span>
                </div>
                <div>
                  <p className="font-medium">{user.full_name || "Unnamed"}</p>
                  <p className="text-sm text-muted-foreground">{user.email}</p>
                </div>
              </div>
            </TableCell>
            <TableCell>
              <Badge variant={user.is_staff ? "default" : "secondary"}>
                {user.is_staff ? "Admin" : "Member"}
              </Badge>
            </TableCell>
            <TableCell>
              <Badge variant={user.is_active ? "default" : "destructive"}>
                {user.is_active ? "Active" : "Inactive"}
              </Badge>
            </TableCell>
            <TableCell>
              <span className="text-sm text-muted-foreground">
                {user.last_login ? format(new Date(user.last_login), "MMM d, yyyy") : "Never"}
              </span>
            </TableCell>
            <TableCell>
              <StaffActionsMenu
                user={user as unknown as User}
                onEdit={onEdit}
                onResetPassword={onResetPassword}
                onResendInvitation={onResendInvitation}
                onToggleStatus={onToggleStatus}
                onRemove={onRemove}
              />
            </TableCell>
          </TableRow>
        ))}
      </TableBody>
    </Table>
  );
}