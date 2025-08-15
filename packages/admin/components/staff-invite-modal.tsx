"use client";

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
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@karrio/ui/components/ui/select";

interface StaffInviteModalProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  onSubmit: (e: React.FormEvent<HTMLFormElement>) => void;
  isLoading: boolean;
}

export function StaffInviteModal({
  open,
  onOpenChange,
  onSubmit,
  isLoading,
}: StaffInviteModalProps) {
  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="max-w-md max-h-[90vh] p-0 flex flex-col">
        {/* Sticky Header */}
        <DialogHeader className="px-4 py-3 border-b sticky top-0 bg-background z-10">
          <DialogTitle>
            Invite New Staff Member
          </DialogTitle>
          <DialogDescription>
            Send an invitation to join your team. They'll receive an email with setup instructions.
          </DialogDescription>
        </DialogHeader>

        <form onSubmit={onSubmit} className="flex flex-col flex-1 min-h-0">
          {/* Scrollable Body */}
          <div className="flex-1 overflow-y-auto px-4 py-3">
            <div className="space-y-4">
              <div className="space-y-2">
                <Label htmlFor="invite_full_name">Full Name</Label>
                <Input 
                  id="invite_full_name" 
                  name="full_name" 
                  placeholder="Enter their full name"
                  required 
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="invite_email">Email Address</Label>
                <Input 
                  id="invite_email" 
                  name="email" 
                  type="email" 
                  placeholder="their.email@company.com"
                  required 
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="invite_role">Initial Role</Label>
                <Select name="role" defaultValue="member">
                  <SelectTrigger>
                    <SelectValue placeholder="Select their role" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="member">
                      <div className="flex items-center gap-2">
                        <div className="h-2 w-2 rounded-full bg-blue-500" />
                        Member - Basic access
                      </div>
                    </SelectItem>
                    <SelectItem value="developer">
                      <div className="flex items-center gap-2">
                        <div className="h-2 w-2 rounded-full bg-green-500" />
                        Developer - Advanced features
                      </div>
                    </SelectItem>
                    <SelectItem value="admin">
                      <div className="flex items-center gap-2">
                        <div className="h-2 w-2 rounded-full bg-red-500" />
                        Admin - Full system access
                      </div>
                    </SelectItem>
                  </SelectContent>
                </Select>
                <p className="text-xs text-muted-foreground">
                  You can change their role and permissions after they join
                </p>
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
                  Sending...
                </>
              ) : (
                "Send Invitation"
              )}
            </Button>
          </DialogFooter>
        </form>
      </DialogContent>
    </Dialog>
  );
}