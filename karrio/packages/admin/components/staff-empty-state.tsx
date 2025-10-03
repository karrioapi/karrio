"use client";

import { Button } from "@karrio/ui/components/ui/button";
import { UserPlus } from "lucide-react";

interface StaffEmptyStateProps {
  onInvite: () => void;
}

export function StaffEmptyState({ onInvite }: StaffEmptyStateProps) {
  return (
    <div className="flex flex-col items-center justify-center py-12 text-center">
      <UserPlus className="h-12 w-12 text-muted-foreground mb-4" />
      <p className="text-lg font-semibold">No staff members yet</p>
      <p className="text-sm text-muted-foreground mb-4">
        Invite your first team member to get started
      </p>
      <Button onClick={onInvite} className="gap-2">
        <UserPlus className="h-4 w-4" />
        Invite Staff Member
      </Button>
    </div>
  );
}