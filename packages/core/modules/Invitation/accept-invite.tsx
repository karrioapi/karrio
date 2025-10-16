"use client";
import { useOrganizationInvitation } from "@karrio/hooks/organization";
import { Button } from "@karrio/ui/components/ui/button";
import { Spinner } from "@karrio/ui/core/components/spinner";
import { Card, CardContent } from "@karrio/ui/components/ui/card";
import { Alert, AlertDescription } from "@karrio/ui/components/ui/alert";
import { useRouter, useSearchParams } from "next/navigation";
import { useSession, getSession } from "next-auth/react";
import { useToast } from "@karrio/ui/hooks/use-toast";
import { useKarrio } from "@karrio/hooks/karrio";
import React, { Suspense, useEffect, useState } from "react";
import { isNone } from "@karrio/lib";
import Link from "next/link";

// Inner component that uses useSearchParams
function AcceptInvitePage() {
  const { data: session, status } = useSession();
  const router = useRouter();
  const searchParams = useSearchParams();
  const token = searchParams.get("token");
  const karrio = useKarrio();
  const { toast } = useToast();
  const {
    query: { data: { organization_invitation } = {}, ...query },
  } = useOrganizationInvitation(token as string);
  const [isAccepting, setIsAccepting] = useState(false);

  useEffect(() => {
    const called = query.isFetched;
    const invite = organization_invitation;

    // Only decide redirects once session status is resolved
    if (!called || status === "loading") return;

    // If there is no active session and invitee doesn't exist, redirect to the signup page (preserve invitation token)
    if (status === "unauthenticated" && invite && !invite?.invitee) {
      setTimeout(
        () =>
          router.push(
            `/signup?email=${encodeURIComponent(
              invite?.invitee_identifier || "",
            )}&next=${encodeURIComponent(`/accept-invitation?token=${token}`)}`,
          ),
        500,
      );
      return;
    }
    // If there is no active session and invitee exist, redirect to the login page
    if (status === "unauthenticated" && invite && invite?.invitee) {
      setTimeout(
        () =>
          router.push(
            `/signin?email=${encodeURIComponent(invite?.invitee?.email || "")}\u0026next=${encodeURIComponent(`/accept-invite?token=${token}`)}`,
          ),
        500,
      );
      return;
    }
    // If there is an active session, stay on this page; we'll render Accept/Decline inline
    if (called && !isNone(session) && invite) {
      return;
    }
  }, [status, session, organization_invitation, token, router, query.isFetched]);

  return (
    <React.Fragment>
      <div className="px-4">
        <Card className="mx-auto mt-6 w-full max-w-md md:max-w-lg lg:max-w-xl border-0 bg-transparent shadow-none sm:border sm:bg-card sm:shadow">
          <CardContent className="p-6 sm:p-6 md:p-8 text-center space-y-3">
            {!query.isFetched && query.isFetching && <Spinner />}

            {query.isFetched && (query.error || !organization_invitation) && (
              <Alert variant="destructive">
                <AlertDescription>
                  Error, invalid or expired organization invitation token!
                </AlertDescription>
              </Alert>
            )}

            {!isNone(session) && organization_invitation && (
              <div className="space-y-4">
                <p>
                  You have been invited to join <strong>{organization_invitation.organization_name}</strong>
                  {" "}as <strong>{organization_invitation.invitee_identifier}</strong>.
                </p>
                {(() => {
                  const inviteeEmail = organization_invitation?.invitee?.email as string | undefined;
                  const currentEmail = (session as any)?.user?.email as string | undefined;
                  return !!inviteeEmail && !!currentEmail && inviteeEmail !== currentEmail;
                })() ? (
                  <div className="space-y-2">
                    <p className="text-sm text-muted-foreground">You're signed in as <strong>{(session as any)?.user?.email}</strong>, but this invitation is for <strong>{organization_invitation?.invitee?.email}</strong>.</p>
                    <div className="flex items-center justify-center gap-2">
                      <Button
                        variant="secondary"
                        onClick={() => {
                          const target = `/signin?email=${encodeURIComponent((organization_invitation?.invitee?.email as string) || "")}&next=${encodeURIComponent(`/accept-invite?token=${token}`)}`;
                          window.location.href = target;
                        }}
                      >
                        Sign in as {organization_invitation?.invitee?.email}
                      </Button>
                      <Button
                        variant="ghost"
                        onClick={() => router.push(`/`)}
                      >
                        Cancel
                      </Button>
                    </div>
                  </div>
                ) : (
                  <div className="flex items-center justify-center gap-2">
                    <Button
                      variant="secondary"
                      disabled={isAccepting}
                      onClick={() => {
                        try {
                          const url = new URL(window.location.href);
                          url.searchParams.delete("token");
                          url.searchParams.delete("accept_invitation");
                          window.location.replace(url.toString());
                        } catch {
                          router.push("/");
                        }
                      }}
                    >
                      Decline
                    </Button>
                    <Button
                      disabled={status !== "authenticated" || isAccepting}
                      onClick={async () => {
                        try {
                          setIsAccepting(true);
                          // Ensure session token is available
                          const s = (await getSession()) as any;
                          const accessToken = s?.accessToken as string | undefined;
                          if (!accessToken) { setIsAccepting(false); return; }

                          const endpoint = `${(karrio as any)?.config?.basePath || ""}/graphql`;
                          const mutation = `mutation accept_organization_invitation($data: AcceptOrganizationInvitationMutationInput!) {\n  accept_organization_invitation(input: $data) {\n    organization { id }\n    errors { field messages }\n  }\n}`;
                          const res = await fetch(endpoint, {
                            method: "POST",
                            headers: {
                              "Content-Type": "application/json",
                              Accept: "application/json",
                              Authorization: `Bearer ${accessToken}`,
                            },
                            body: JSON.stringify({ query: mutation, variables: { data: { guid: token } } }),
                          });
                          const body = await res.json();
                          if (body?.errors) throw new Error("Failed to accept invitation");
                          const orgName = organization_invitation?.organization_name || "the organization";
                          toast({ title: "Invite Accepted", description: `Welcome to ${orgName}` });
                          router.push("/");
                        } catch {
                          setIsAccepting(false);
                        }
                      }}
                    >
                      {isAccepting ? "Accepting..." : "Accept Invitation"}
                    </Button>
                  </div>
                )}
              </div>
            )}
          </CardContent>
        </Card>
      </div>

      {query.error ? (
        <div className="my-4 text-center text-sm">
          Return to {" "}
          <Link href="/signin" className="font-semibold text-primary hover:underline">
            Sign in
          </Link>
        </div>
      ) : null}
    </React.Fragment>
  );
}

// Exported component with Suspense
export default function Page() {
  return (
    <Suspense fallback={
      <div className="card isolated-card my-6">
        <div className="card-content has-text-centered">
          <Spinner />
        </div>
      </div>
    }>
      <AcceptInvitePage />
    </Suspense>
  );
}
