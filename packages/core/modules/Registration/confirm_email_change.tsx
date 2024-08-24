"use client";
import { dynamicMetadata } from "@karrio/core/components/metadata";
import { Spinner } from "@karrio/ui/components/spinner";
import { useUserMutation } from "@karrio/hooks/user";
import { useSearchParams } from "next/navigation";
import React, { useEffect } from "react";
import { isNone } from "@karrio/lib";
import Link from "next/link";

export const generateMetadata = dynamicMetadata("Email Change Confirmation");

export default function Page(pageProps: any) {
  const Component: React.FC = () => {
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
  };

  return (
    <>
      <Component />
    </>
  );
}
