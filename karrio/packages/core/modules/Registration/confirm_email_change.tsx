"use client";
import React, { Suspense, useEffect } from "react";
import Link from "next/link";
import { useSearchParams } from "next/navigation";
import { useUserMutation } from "@karrio/hooks/user";
import { isNone } from "@karrio/lib";
import { Spinner } from "@karrio/ui/core/components/spinner";
import { Card, CardContent } from "@karrio/ui/components/ui/card";
import { Alert, AlertDescription } from "@karrio/ui/components/ui/alert";

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
      <div className="px-4">
        <Card className="mx-auto mt-6 w-full max-w-md md:max-w-lg lg:max-w-xl border-0 bg-transparent shadow-none sm:border sm:bg-card sm:shadow">
          <CardContent className="p-6 sm:p-6 md:p-8 text-center space-y-3">
          {loading && <Spinner />}

          {!loading && success === true && (
            <p>
              Your email has been changed to <strong>{email}</strong>!
            </p>
          )}
          {!loading && success === false && (
            <Alert variant="destructive">
              <AlertDescription>
                Error, invalid or expired email change token!
              </AlertDescription>
            </Alert>
          )}
          </CardContent>
        </Card>
      </div>

      <div className="my-4 text-center text-sm">
        <Link href="/" className="font-semibold text-primary hover:underline">
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
      <Card className="mx-auto my-6 w-full max-w-md"><CardContent className="pt-6 text-center"><Spinner /></CardContent></Card>
    }>
      <EmailChangeConfirmation />
    </Suspense>
  );
}
