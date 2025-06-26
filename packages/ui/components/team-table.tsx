"use client";

import { useState } from "react";
import { formatDateTimeLong } from "@karrio/lib";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow
} from "./ui/table";
import { Badge } from "./ui/badge";
import { Button } from "./ui/button";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "./ui/dropdown-menu";
import { Avatar, AvatarFallback } from "./ui/avatar";
import { ConfirmationDialog } from "./confirmation-dialog";
import { RoleManagementDialog } from "./role-management-dialog";
import { MoreHorizontal, Trash2, UserCog } from "lucide-react";

interface TeamMember {
  email: string;
  full_name?: string | null;
  is_admin: boolean;
  is_owner: boolean | null;
  last_login?: string | null;
  is_active?: boolean;
  user_id?: string | null;
  invitation?: {
    id: string;
    invitee_identifier: string;
  } | null;
}

interface TeamTableProps {
  members: TeamMember[];
  currentUserEmail: string;
  isCurrentUserAdmin: boolean;
  onRemoveInvitation: (id: string) => void;
  onRemoveMember?: (userId: string) => void;
  onToggleMemberStatus?: (userId: string, isActive: boolean) => void;
  onResendInvitation?: (invitationId: string) => void;
  onUpdateRole?: (userId: string, roles: string[]) => void;
}

export function TeamTable({
  members,
  currentUserEmail,
  isCurrentUserAdmin,
  onRemoveInvitation,
  onRemoveMember,
  onToggleMemberStatus,
  onResendInvitation,
  onUpdateRole
}: TeamTableProps) {
  const [confirmDialogOpen, setConfirmDialogOpen] = useState(false);
  const [invitationToRemove, setInvitationToRemove] = useState<{ id: string, email: string } | null>(null);
  const [memberToRemove, setMemberToRemove] = useState<{ userId: string, email: string } | null>(null);
  const [memberToToggle, setMemberToToggle] = useState<{ userId: string, email: string, currentStatus: boolean } | null>(null);
  const [roleDialogOpen, setRoleDialogOpen] = useState(false);
  const [memberToManageRole, setMemberToManageRole] = useState<TeamMember | null>(null);

  const getInitials = (name?: string | null, email?: string) => {
    if (name) {
      return name.split(' ').map(n => n[0]).join('').toUpperCase().slice(0, 2);
    }
    if (email) {
      return email.slice(0, 2).toUpperCase();
    }
    return 'U';
  };

  const handleRemoveClick = (invitation: { id: string, invitee_identifier: string }) => {
    setInvitationToRemove({
      id: invitation.id,
      email: invitation.invitee_identifier
    });
    setConfirmDialogOpen(true);
  };

  const handleConfirmRemove = () => {
    if (invitationToRemove) {
      onRemoveInvitation(invitationToRemove.id);
      setInvitationToRemove(null);
    }
    if (memberToRemove && onRemoveMember) {
      onRemoveMember(memberToRemove.userId);
      setMemberToRemove(null);
    }
    if (memberToToggle && onToggleMemberStatus) {
      onToggleMemberStatus(memberToToggle.userId, !memberToToggle.currentStatus);
      setMemberToToggle(null);
    }
  };

  const handleRemoveMemberClick = (member: TeamMember) => {
    // Use user_id if available, otherwise use email as identifier
    const userId = member.user_id || member.email;
    setMemberToRemove({
      userId: userId,
      email: member.email
    });
    setConfirmDialogOpen(true);
  };

  const handleToggleMemberClick = (member: TeamMember) => {
    // Use user_id if available, otherwise use email as identifier
    const userId = member.user_id || member.email;
    setMemberToToggle({
      userId: userId,
      email: member.email,
      currentStatus: member.is_active ?? true
    });
    setConfirmDialogOpen(true);
  };

  const handleResendClick = (invitationId: string) => {
    if (onResendInvitation) {
      onResendInvitation(invitationId);
    }
  };

  const handleManageRoleClick = (member: TeamMember) => {
    setMemberToManageRole(member);
    setRoleDialogOpen(true);
  };

  const handleUpdateRole = (userId: string, roles: string[]) => {
    if (onUpdateRole) {
      onUpdateRole(userId, roles);
    }
  };

  const getRoleBadges = (member: TeamMember) => {
    const badges = [];

    if (member.is_owner) {
      badges.push(
        <Badge key="owner" variant="default" className="text-xs">
          Owner
        </Badge>
      );
    }

    if (member.is_admin) {
      badges.push(
        <Badge key="admin" variant="secondary" className="text-xs">
          Admin
        </Badge>
      );
    }

    if (!member.is_admin && !member.is_owner) {
      badges.push(
        <Badge key="viewer" variant="outline" className="text-xs">
          View Only
        </Badge>
      );
    }

    return badges;
  };

  return (
    <div className="space-y-4">
      <div className="rounded-md border">
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead className="w-[300px]">Member</TableHead>
              <TableHead>Role</TableHead>
              <TableHead>Last Login</TableHead>
              <TableHead className="w-[50px]"></TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {members.map((member) => (
              <TableRow key={`${member.email}-${Date.now()}`} className="h-16">
                <TableCell>
                  <div className="flex items-center space-x-3">
                    <Avatar className="h-8 w-8">
                      <AvatarFallback className="text-xs">
                        {getInitials(member.full_name, member.email)}
                      </AvatarFallback>
                    </Avatar>
                    <div className="space-y-1">
                      <div className="flex items-center space-x-2">
                        {member.full_name && (
                          <span className="text-sm font-medium">
                            {member.full_name}
                          </span>
                        )}
                        {member.email === currentUserEmail && (
                          <Badge variant="outline" className="text-xs px-2">
                            You
                          </Badge>
                        )}
                      </div>
                      <p className="text-sm text-muted-foreground">
                        {member.email}
                      </p>
                    </div>
                  </div>
                </TableCell>
                <TableCell>
                  <div className="flex flex-wrap gap-1">
                    {getRoleBadges(member)}
                  </div>
                </TableCell>
                <TableCell>
                  {member.last_login ? (
                    <span className="text-sm text-muted-foreground">
                      {formatDateTimeLong(member.last_login)}
                    </span>
                  ) : member.invitation ? (
                    <Badge variant="outline" className="text-xs">
                      Invitation sent
                    </Badge>
                  ) : (
                    <span className="text-sm text-muted-foreground">Never</span>
                  )}
                </TableCell>
                <TableCell>
                  {(() => {
                    const isCurrentUser = member.email === currentUserEmail;
                    const canManageThisMember = isCurrentUserAdmin &&
                      !isCurrentUser &&
                      !member.is_owner;

                    return canManageThisMember ? (
                      <DropdownMenu>
                        <DropdownMenuTrigger asChild>
                          <Button variant="ghost" size="sm" className="h-8 w-8 p-0">
                            <MoreHorizontal className="h-4 w-4" />
                            <span className="sr-only">Open menu</span>
                          </Button>
                        </DropdownMenuTrigger>
                        <DropdownMenuContent align="end">
                          {member.invitation ? (
                            <>
                              <DropdownMenuItem
                                onClick={() => handleResendClick(member.invitation!.id)}
                              >
                                Resend invitation
                              </DropdownMenuItem>
                              <DropdownMenuItem
                                onClick={() => handleRemoveClick(member.invitation!)}
                                className="text-destructive focus:text-destructive"
                              >
                                <Trash2 className="mr-2 h-4 w-4" />
                                Remove invitation
                              </DropdownMenuItem>
                            </>
                          ) : (
                            <>
                              <DropdownMenuItem
                                onClick={() => handleManageRoleClick(member)}
                              >
                                <UserCog className="mr-2 h-4 w-4" />
                                Manage role
                              </DropdownMenuItem>
                              <DropdownMenuItem
                                onClick={() => handleToggleMemberClick(member)}
                              >
                                {member.is_active === false ? 'Activate' : 'Suspend'} member
                              </DropdownMenuItem>
                              <DropdownMenuItem
                                onClick={() => handleRemoveMemberClick(member)}
                                className="text-destructive focus:text-destructive"
                              >
                                <Trash2 className="mr-2 h-4 w-4" />
                                Remove member
                              </DropdownMenuItem>
                            </>
                          )}
                        </DropdownMenuContent>
                      </DropdownMenu>
                    ) : null;
                  })()}
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </div>

      <div className="flex items-center justify-between text-sm text-muted-foreground">
        <span className="font-medium">{members.length} results</span>
        <div className="flex space-x-2">
          <Button variant="outline" size="sm" disabled>
            Previous
          </Button>
          <Button variant="outline" size="sm" disabled>
            Next
          </Button>
        </div>
      </div>

      <ConfirmationDialog
        open={confirmDialogOpen}
        onOpenChange={setConfirmDialogOpen}
        title={
          invitationToRemove ? "Remove invitation" :
            memberToRemove ? "Remove member" :
              memberToToggle ? (memberToToggle.currentStatus ? "Suspend member" : "Activate member") :
                "Confirm action"
        }
        description={
          invitationToRemove ? `Are you sure you want to remove the invitation for ${invitationToRemove.email}? This action cannot be undone.` :
            memberToRemove ? `Are you sure you want to remove ${memberToRemove.email} from the organization? This action cannot be undone.` :
              memberToToggle ? `Are you sure you want to ${memberToToggle.currentStatus ? 'suspend' : 'activate'} ${memberToToggle.email}?` :
                "Are you sure you want to perform this action?"
        }
        confirmLabel={
          invitationToRemove ? "Remove" :
            memberToRemove ? "Remove" :
              memberToToggle ? (memberToToggle.currentStatus ? "Suspend" : "Activate") :
                "Confirm"
        }
        onConfirm={handleConfirmRemove}
      />

      <RoleManagementDialog
        open={roleDialogOpen}
        onOpenChange={setRoleDialogOpen}
        member={memberToManageRole}
        onUpdateRole={handleUpdateRole}
      />
    </div>
  );
}
