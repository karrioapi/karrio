"use client";
import { useOrganizationInvitation } from "@karrio/hooks/organization";
import { Spinner } from "@karrio/ui/core/components/spinner";
import { Card, CardContent } from "@karrio/ui/components/ui/card";
import { Alert, AlertDescription } from "@karrio/ui/components/ui/alert";
import { useRouter, useSearchParams } from "next/navigation";
import { useSession } from "next-auth/react";
import React, { Suspense, useEffect } from "react";
import { isNone } from "@karrio/lib";
import Link from "next/link";

// Inner component that uses useSearchParams
function AcceptInvitePage() {
  const { data: session } = useSession();
  const router = useRouter();
  const searchParams = useSearchParams();
  const token = searchParams.get("token");
  const {
    query: { data: { organization_invitation } = {}, ...query },
  } = useOrganizationInvitation(token as string);

  useEffect(() => {
    const called = query.isFetched;
    const invite = organization_invitation;

    // If there is no active session and invitee doesn't exist, redirect to the signup page (preserve invitation token)
    if (called && isNone(session) && invite && !invite?.invitee) {
      setTimeout(
        () =>
          router.push(
            `/signup?email=${encodeURIComponent(
              invite?.invitee_identifier || "",
            )}&next=${encodeURIComponent(`/accept-invite?token=${token}`)}`,
          ),
        1000,
      );
      return;
    }
    // If there is no active session and invitee exist, redirect to the login page
    if (called && isNone(session) && invite && invite?.invitee) {
      setTimeout(
        () =>
          router.push(
            `/signin?email=${encodeURIComponent(invite?.invitee?.email || "")}\u0026next=${encodeURIComponent(`/?accept_invitation=${token}`)}`,
          ),
        1000,
      );
      return;
    }
    // If there is an active session, redirect to the dashboard
    if (called && !isNone(session) && invite) {
      setTimeout(() => router.push(`/?accept_invitation=${token}`), 1000);
      return;
    }
  }, [session, organization_invitation, token, router]);

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

            {organization_invitation && <p>Redirecting...</p>}
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
