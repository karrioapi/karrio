"use client";
import { useOrganizationInvitation } from "@karrio/hooks/organization";
import { Spinner } from "@karrio/ui/core/components/spinner";
import { useRouter, useSearchParams } from "next/navigation";
import { useSession } from "next-auth/react";
import React, { useEffect } from "react";
import { isNone } from "@karrio/lib";
import Link from "next/link";


export default function Page() {
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

    // If there is no active session and invitee doesn't exist, redirect to the signup page
    if (called && isNone(session) && invite && !invite?.invitee) {
      setTimeout(
        () => router.push(`/signup?email=${invite?.invitee_identifier}`),
        1000,
      );
      return;
    }
    // If there is no active session and invitee exist, redirect to the login page
    if (called && isNone(session) && invite && invite?.invitee) {
      setTimeout(
        () =>
          router.push(
            `/signin?email=${invite?.invitee?.email}&next=/?accept_invitation=${token}`,
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
      <div className="card isolated-card my-6">
        <div className="card-content has-text-centered ">
          {!query.isFetched && query.isFetching && <Spinner />}

          {query.isFetched && (query.error || !organization_invitation) && (
            <p>Error, invalid or expired organization invitation token!</p>
          )}

          {organization_invitation && <p>Redirecting...</p>}
        </div>
      </div>

      {query.error ? (
        <div className="has-text-centered my-4 is-size-6">
          <span>
            Return to{" "}
            <Link legacyBehavior href="/signin">
              Sign in
            </Link>
          </span>
        </div>
      ) : (
        <></>
      )}
    </React.Fragment>
  );
}
