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
import { useOrganizationInvitation, useOrganizationMutation } from "@karrio/hooks/organization";
import { useToast } from "@karrio/ui/hooks/use-toast";
import { createContext, useContext, useState, useEffect } from "react";
import { useSearchParams } from "next/navigation";
import { signIn } from "next-auth/react";

interface AcceptInvitationDialogContextType {
  acceptInvitation: () => void;
}

const AcceptInvitationDialogContext = createContext<AcceptInvitationDialogContextType>(
  {} as AcceptInvitationDialogContextType,
);

export const AcceptInvitationDialogProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [isOpen, setIsOpen] = useState<boolean>(false);

  const acceptInvitation = () => {
    setIsOpen(true);
  };

  const close = () => {
    setIsOpen(false);
  }

  return (
    <AcceptInvitationDialogContext.Provider value={{ acceptInvitation }}>
      {children}
      {isOpen && <AcceptInvitationDialog close={close} />}
    </AcceptInvitationDialogContext.Provider>
  );
};

const AcceptInvitationDialog: React.FC<{ close: () => void }> = ({ close }) => {
  const searchParams = useSearchParams();
  const guid = searchParams.get('token') as string;
  const { toast } = useToast();
  const { data: { invitation } = {}, isLoading, isError } = useOrganizationInvitation(guid) as any;
  const { acceptInvitation: mutation } = useOrganizationMutation() as any;
  const [fullName, setFullName] = useState("");
  const [password, setPassword] = useState("");

  useEffect(() => {
    if (invitation?.invitee_identifier) {
      // Assuming the identifier is an email, pre-fill the name from it
      const nameFromEmail = invitation.invitee_identifier.split('@')[0].replace(/[._-]/g, ' ').replace(/\b\w/g, (l: string) => l.toUpperCase());
      setFullName(nameFromEmail);
    }
  }, [invitation]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!fullName || !password) return;

    try {
      const { acceptInvitation: result } = await mutation.mutateAsync({
        guid,
        full_name: fullName,
        password,
      }) as any;

      if (result?.errors && result.errors.length > 0) {
        throw new Error(result.errors.map((e: any) => e.messages).join(', '));
      }

      toast({
        title: "Invitation accepted!",
        description: "You have successfully joined the organization.",
      });

      // Sign in the user
      await signIn("credentials", {
        email: invitation.invitee_identifier,
        password: password,
        redirect: false,
      });

      close();
      window.location.reload();

    } catch (error: any) {
      toast({
        variant: "destructive",
        title: "Error accepting invitation",
        description: error.message,
      });
    }
  };

  return (
    <Dialog open={true} onOpenChange={(isOpen) => !isOpen && close()}>
      <DialogContent className="sm:max-w-[425px]">
        <DialogHeader>
          <DialogTitle>Accept Invitation</DialogTitle>
          <DialogDescription>
            {isError ? "Invalid or expired invitation token." : "You have been invited to join an organization."}
          </DialogDescription>
        </DialogHeader>

        {isLoading && <p>Loading invitation details...</p>}

        {!isLoading && !isError && invitation && (
          <form onSubmit={handleSubmit} className="space-y-4">
            <p>You have been invited by <strong>{invitation.inviter_name}</strong> to join <strong>{invitation.organization_name}</strong>.</p>
            <p>Accept the invitation for <strong>{invitation.invitee_identifier}</strong> by setting up your account below.</p>

            <div className="grid gap-4 py-4">
              <div className="grid grid-cols-4 items-center gap-4">
                <Label htmlFor="full_name" className="text-right">
                  Full Name
                </Label>
                <Input
                  id="full_name"
                  value={fullName}
                  onChange={(e) => setFullName(e.target.value)}
                  className="col-span-3"
                  required
                />
              </div>
              <div className="grid grid-cols-4 items-center gap-4">
                <Label htmlFor="password" className="text-right">
                  Password
                </Label>
                <Input
                  id="password"
                  type="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  className="col-span-3"
                  required
                />
              </div>
            </div>

            <DialogFooter>
              <Button type="button" variant="ghost" onClick={close}>
                Cancel
              </Button>
              <Button type="submit" disabled={mutation.isLoading}>
                {mutation.isLoading ? "Accepting..." : "Accept & Join"}
              </Button>
            </DialogFooter>
          </form>
        )}
      </DialogContent>
    </Dialog >
  );
}


export function useAcceptInvitationDialog() {
  return useContext(AcceptInvitationDialogContext);
}
