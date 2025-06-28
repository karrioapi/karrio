"use client";

import { useState } from "react";
import { Button } from "./ui/button";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "./ui/dialog";
import { Input } from "./ui/input";
import { Label } from "./ui/label";
import { Badge } from "./ui/badge";
import { UserPlus, X } from "lucide-react";

interface InviteMemberDialogProps {
  onInvite: (emails: string[]) => Promise<void>;
  isLoading?: boolean;
  children?: React.ReactNode;
}

export function InviteMemberDialog({ onInvite, isLoading, children }: InviteMemberDialogProps) {
  const [open, setOpen] = useState(false);
  const [emailInput, setEmailInput] = useState("");
  const [emails, setEmails] = useState<string[]>([]);
  const [error, setError] = useState("");

  const isValidEmail = (email: string) => {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
  };

  const addEmail = () => {
    const trimmedEmail = emailInput.trim().toLowerCase();

    if (!trimmedEmail) {
      setError("Please enter an email address");
      return;
    }

    if (!isValidEmail(trimmedEmail)) {
      setError("Please enter a valid email address");
      return;
    }

    if (emails.includes(trimmedEmail)) {
      setError("This email has already been added");
      return;
    }

    setEmails([...emails, trimmedEmail]);
    setEmailInput("");
    setError("");
  };

  const removeEmail = (emailToRemove: string) => {
    setEmails(emails.filter(email => email !== emailToRemove));
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === "Enter") {
      e.preventDefault();
      addEmail();
    }
  };

  const handleInvite = async () => {
    if (emails.length === 0) {
      setError("Please add at least one email address");
      return;
    }

    try {
      await onInvite(emails);
      setEmails([]);
      setEmailInput("");
      setError("");
      setOpen(false);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to send invitations");
    }
  };

  const reset = () => {
    setEmails([]);
    setEmailInput("");
    setError("");
  };

  return (
    <Dialog open={open} onOpenChange={(newOpen) => {
      setOpen(newOpen);
      if (!newOpen) reset();
    }}>
      <DialogTrigger asChild>
        {children || (
          <Button size="sm">
            <UserPlus className="mr-2 h-4 w-4" />
            New member
          </Button>
        )}
      </DialogTrigger>
      <DialogContent className="sm:max-w-md p-4 pb-8">
        <DialogHeader>
          <DialogTitle>Invite team members</DialogTitle>
          <DialogDescription>
            Invite new members to join your organization. They'll receive an email invitation.
          </DialogDescription>
        </DialogHeader>

        <div className="space-y-4">
          <div className="space-y-2">
            <Label htmlFor="email">Email addresses</Label>
            <div className="flex space-x-2">
              <Input
                id="email"
                type="email"
                placeholder="Enter email address"
                value={emailInput}
                onChange={(e) => setEmailInput(e.target.value)}
                onKeyPress={handleKeyPress}
                className="flex-1"
              />
              <Button
                type="button"
                variant="outline"
                onClick={addEmail}
                disabled={!emailInput.trim()}
              >
                Add
              </Button>
            </div>
            {error && (
              <p className="text-sm text-destructive">{error}</p>
            )}
          </div>

          {emails.length > 0 && (
            <div className="space-y-2">
              <Label>Invitations to send ({emails.length})</Label>
              <div className="flex flex-wrap gap-2 p-3 bg-muted rounded-md min-h-[3rem]">
                {emails.map((email) => (
                  <Badge key={email} variant="secondary" className="flex items-center gap-1">
                    {email}
                    <button
                      type="button"
                      onClick={() => removeEmail(email)}
                      className="ml-1 hover:bg-secondary-foreground/20 rounded-full p-0.5"
                    >
                      <X className="h-3 w-3" />
                    </button>
                  </Badge>
                ))}
              </div>
            </div>
          )}

          <div className="flex justify-end space-x-2">
            <Button
              variant="outline"
              onClick={() => setOpen(false)}
              disabled={isLoading}
            >
              Cancel
            </Button>
            <Button
              onClick={handleInvite}
              disabled={emails.length === 0 || isLoading}
            >
              {isLoading ? "Sending..." : `Send invitation${emails.length > 1 ? 's' : ''}`}
            </Button>
          </div>
        </div>
      </DialogContent>
    </Dialog>
  );
}
