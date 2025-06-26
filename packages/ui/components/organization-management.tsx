"use client";

import { useOrganizationMutation, useOrganizations } from '@karrio/hooks/organization';
import { OrganizationForm } from './organization-form';
import { TeamTable } from './team-table';
import { InviteMemberDialog } from './invite-member-dialog';
import { NotificationType } from '@karrio/types';
import { Notify } from '../core/components/notifier';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card';
import { Separator } from './ui/separator';
import { Users } from 'lucide-react';
import { useContext } from 'react';

export function OrganizationManagement() {
  const { notify } = useContext(Notify);
  const mutation = useOrganizationMutation();
  const { organization } = useOrganizations();

  const handleUpdateName = async (name: string) => {
    try {
      await mutation.updateOrganization.mutateAsync({
        id: organization?.id as string,
        name,
      });
      notify({
        type: NotificationType.success,
        message: 'Organization name updated successfully!'
      });
    } catch (error: any) {
      notify({
        type: NotificationType.error,
        message: error.message || 'Failed to update organization name'
      });
      throw error;
    }
  };

  const handleInviteMembers = async (emails: string[]) => {
    try {
      await mutation.sendOrganizationInvites.mutateAsync({
        org_id: organization?.id as string,
        emails,
        redirect_url: `${window.location.origin}/accept-invitation`,
        roles: [],
      });
      notify({
        type: NotificationType.success,
        message: `Invitation${emails.length > 1 ? 's' : ''} sent successfully!`
      });
    } catch (error: any) {
      notify({
        type: NotificationType.error,
        message: error.message || 'Failed to send invitations'
      });
      throw error;
    }
  };

  const handleRemoveInvitation = async (id: string) => {
    try {
      await mutation.deleteOrganizationInvitation.mutateAsync({ id });
      notify({
        type: NotificationType.success,
        message: 'Invitation removed successfully!'
      });
    } catch (error: any) {
      notify({
        type: NotificationType.error,
        message: error.message || 'Failed to remove invitation'
      });
    }
  };

  const handleRemoveMember = async (userId: string) => {
    try {
      await mutation.removeOrganizationMember.mutateAsync({
        org_id: organization?.id as string,
        user_id: userId,
      });
      notify({
        type: NotificationType.success,
        message: 'Member removed successfully!'
      });
    } catch (error: any) {
      notify({
        type: NotificationType.error,
        message: error.message || 'Failed to remove member'
      });
    }
  };

  const handleToggleMemberStatus = async (userId: string, isActive: boolean) => {
    try {
      await mutation.updateMemberStatus.mutateAsync({
        org_id: organization?.id as string,
        user_id: userId,
        is_active: isActive,
      });
      notify({
        type: NotificationType.success,
        message: `Member ${isActive ? 'activated' : 'suspended'} successfully!`
      });
    } catch (error: any) {
      notify({
        type: NotificationType.error,
        message: error.message || `Failed to ${isActive ? 'activate' : 'suspend'} member`
      });
    }
  };

  const handleResendInvitation = async (invitationId: string) => {
    try {
      await mutation.resendOrganizationInvite.mutateAsync({
        invitation_id: invitationId,
        redirect_url: `${window.location.origin}/accept-invitation`,
      });
      notify({
        type: NotificationType.success,
        message: 'Invitation resent successfully!'
      });
    } catch (error: any) {
      notify({
        type: NotificationType.error,
        message: error.message || 'Failed to resend invitation'
      });
    }
  };

  const handleUpdateRole = async (userId: string, roles: string[]) => {
    try {
      await mutation.setOrganizationUserRoles.mutateAsync({
        org_id: organization?.id as string,
        user_id: userId,
        roles: roles as any, // Convert to the expected enum type
      });
      notify({
        type: NotificationType.success,
        message: 'User role updated successfully!'
      });
    } catch (error: any) {
      notify({
        type: NotificationType.error,
        message: error.message || 'Failed to update user role'
      });
    }
  };

  if (!organization) {
    return null;
  }

  const isCurrentUserAdmin = Boolean(organization.current_user?.is_admin || organization.current_user?.is_owner);

  return (
    <div className="space-y-8">
      {/* Organization Settings */}
      <OrganizationForm
        initialName={organization.name}
        onSave={handleUpdateName}
        isLoading={mutation.updateOrganization.isLoading}
      />

      {/* Team Management */}
      <Card>
        <CardHeader>
          <div className="flex items-center justify-between">
            <div>
              <CardTitle className="flex items-center gap-2">
                <Users className="h-5 w-5" />
                Team
              </CardTitle>
              <CardDescription>
                Manage your organization's team members and their permissions.
              </CardDescription>
            </div>
            {isCurrentUserAdmin && (
              <InviteMemberDialog
                onInvite={handleInviteMembers}
                isLoading={mutation.sendOrganizationInvites.isLoading}
              />
            )}
          </div>
        </CardHeader>
        <CardContent>
          <TeamTable
            members={organization.members || []}
            currentUserEmail={organization.current_user?.email || ''}
            isCurrentUserAdmin={isCurrentUserAdmin}
            onRemoveInvitation={handleRemoveInvitation}
            onRemoveMember={handleRemoveMember}
            onToggleMemberStatus={handleToggleMemberStatus}
            onResendInvitation={handleResendInvitation}
            onUpdateRole={handleUpdateRole}
          />
        </CardContent>
      </Card>
    </div>
  );
}
