"use client";

import { useToast } from "@karrio/insiders/hooks/use-toast";
import { trpc } from "@karrio/console/trpc/client";
import { useRouter } from "next/navigation";
import { useEffect } from "react";

export default function InvitePage({ params }: { params: { token: string } }) {
  const router = useRouter();
  const { toast } = useToast();
  const acceptInvitation = trpc.organizations.acceptInvitation.useMutation({
    onSuccess: (org) => {
      toast({
        title: "Welcome!",
        description: `You've joined ${org.name}`,
      });
      router.push(`/orgs/${org.id}`);
    },
    onError: (error) => {
      toast({
        title: "Error",
        description: error.message,
        variant: "destructive",
      });
      router.push("/orgs");
    },
  });

  useEffect(() => {
    acceptInvitation.mutate({ token: params.token });
  }, [params.token]);

  return (
    <div className="flex min-h-screen items-center justify-center">
      <div className="text-center">
        <h1 className="text-2xl font-semibold mb-2">Accepting invitation...</h1>
        <p className="text-muted-foreground">
          Please wait while we process your invitation.
        </p>
      </div>
    </div>
  );
}
