"use client";
import { Spinner } from "@karrio/ui/core/components/spinner";
import { useUserMutation } from "@karrio/hooks/user";
import { useSearchParams } from "next/navigation";
import React, { Suspense, useEffect } from "react";
import { isNone } from "@karrio/lib";
import Link from "next/link";

// Inner component that uses useSearchParams
function EmailChangeConfirmation(): JSX.Element {
  const searchParams = useSearchParams();
  const token = searchParams.get("token") as string;
  const { confirmEmailChange } = useUserMutation();
  const [loading, setLoading] = React.useState(false);
  const [success, setSuccess] = React.useState(false);
  const [email, setEmail] = React.useState("");

  const confirm = async () => {
    setLoading(true);
    try {
      const { confirm_email_change } = await confirmEmailChange.mutateAsync({
        token: token as string,
      });
      const email = confirm_email_change.user?.email;
      setSuccess(!isNone(email));
      setEmail(email || "");
    } catch (e) {
      setSuccess(false);
    }
    setLoading(false);
  };

  useEffect(() => {
    if (!isNone(token)) {
      confirm();
    }
  }, [token]);

  return (
    <>
      <div className="card isolated-card my-6">
        <div className="card-content has-text-centered ">
          {loading && <Spinner />}

          {!loading && success === true && (
            <p>
              Your email has been changed to <strong>{email}</strong>!
            </p>
          )}
          {!loading && success === false && (
            <p>Error, invalid or expired email change token!</p>
          )}
        </div>
      </div>

      <div className="has-text-centered my-4 is-size-6">
        <Link legacyBehavior href="/">
          Return Home
        </Link>
      </div>
    </>
  );
}

// Exported component with Suspense
export default function Page(pageProps: any) {
  return (
    <Suspense fallback={
      <div className="card isolated-card my-6">
        <div className="card-content has-text-centered">
          <Spinner />
        </div>
      </div>
    }>
      <EmailChangeConfirmation />
    </Suspense>
  );
}
