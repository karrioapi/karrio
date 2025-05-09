"use client";
import { Spinner } from "@karrio/ui/core/components/spinner";
import { useUserMutation } from "@karrio/hooks/user";
import { useSearchParams } from "next/navigation";
import React, { useEffect } from "react";
import { isNone } from "@karrio/lib";
import Link from "next/link";


export default function Page(pageProps: any) {
  const searchParams = useSearchParams();
  const token = searchParams.get("token") as string;
  const {
    confirmEmail: { isLoading, data, mutateAsync },
  } = useUserMutation();

  useEffect(() => {
    !isNone(token) && mutateAsync({ token });
  }, [token]);

  return (
    <>
      <div className="card isolated-card my-6">
        <div className="card-content has-text-centered ">
          {isLoading && <Spinner />}

          {data?.confirm_email?.success === true && (
            <p>Your account is verified!</p>
          )}

          {!isLoading && !data?.confirm_email?.success && (
            <p>Error, invalid or expired account activation token!</p>
          )}
        </div>
      </div>

      <div className="has-text-centered my-4 is-size-6">
        <Link legacyBehavior href="/signin">
          Sign in
        </Link>
      </div>
    </>
  );
}
