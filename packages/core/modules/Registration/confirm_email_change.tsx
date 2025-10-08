"use client";
import React, { Suspense, useEffect } from "react";
import Link from "next/link";
import { useSearchParams } from "next/navigation";
import { useAPIMetadata } from "@karrio/hooks/api-metadata";
import { isNone, url$ } from "@karrio/lib";
import { Spinner } from "@karrio/ui/core/components/spinner";
import { Card, CardContent } from "@karrio/ui/components/ui/card";
import { Alert, AlertDescription } from "@karrio/ui/components/ui/alert";
import { useSession } from "next-auth/react";
import { useRouter } from "next/navigation";
import axios from "axios";

// Inner component that uses useSearchParams
function EmailChangeConfirmation(): JSX.Element {
  const searchParams = useSearchParams();
  const rawToken = searchParams.get("token") as string;
  const token = (rawToken || "").trim().replace(/^"+|"+$/g, "");
  const { references, getHost, metadata } = useAPIMetadata();
  const { status } = useSession();
  const router = useRouter();
  const [loading, setLoading] = React.useState(false);
  const [success, setSuccess] = React.useState(false);
  const [email, setEmail] = React.useState("");
  const [errorMessage, setErrorMessage] = React.useState<string | null>(null);

  const confirm = async () => {
    setLoading(true);
    try {
      const host = getHost?.();
      const graphqlUrl = (metadata as any)?.GRAPHQL || url$`${host}/graphql`;
      // Build auth headers from the current NextAuth session
      const session = (await import("next-auth/react").then(m => m.getSession())) as any;
      const headers: Record<string, string> = {};
      if (session?.accessToken) headers["authorization"] = `Bearer ${session.accessToken}`;
      if (session?.orgId) headers["x-org-id"] = String(session.orgId);
      if (session?.testMode) headers["x-test-mode"] = "true";

      const { data } = await axios.post(
        graphqlUrl,
        {
          query: `mutation confirm_email_change($data: ConfirmEmailChangeMutationInput!) { confirm_email_change(input: $data) { user { email } errors { field messages } } }`,
          variables: { data: { token } },
        },
        {
          headers,
        }
      );
      const result = data?.data?.confirm_email_change;
      const email = result?.user?.email;
      if (!isNone(email)) {
        setSuccess(true);
        setEmail(email || "");
        setErrorMessage(null);
      } else {
        // Extract GraphQL errors from body when request succeeds with errors
        const graphQLErrors =
          result?.errors || data?.errors || data?.data?.errors || [];
        const detailedMessage = Array.isArray(graphQLErrors)
          ? graphQLErrors
            .map((e: any) =>
              e?.message || (e?.messages ? e.messages.join(" ") : ""),
            )
            .filter(Boolean)
            .join(" | ")
          : undefined;

        setSuccess(false);
        setErrorMessage(detailedMessage || null);
      }
    } catch (e: any) {
      setSuccess(false);
      const message =
        e?.response?.errors?.[0]?.message ||
        e?.response?.data?.errors?.[0]?.message ||
        e?.data?.errors?.[0]?.message ||
        (e?.response?.status ? `${e.response.status} ${e.response.statusText}` : e?.message) ||
        null;
      setErrorMessage(message);
    }
    setLoading(false);
  };

  useEffect(() => {
    const next = window.location.pathname + window.location.search;
    // If next-auth isn't authenticated, redirect
    if (status === "unauthenticated") {
      router.push(`/signin?next=${next}`);
      return;
    }

    // Proceed once NextAuth is authenticated
    if (status === "authenticated" && !isNone(token)) {
      confirm();
    }
  }, [status, token, router]);

  return (
    <>
      <div className="px-4">
        <Card className="mx-auto mt-6 w-full max-w-md md:max-w-lg lg:max-w-xl border-0 bg-transparent shadow-none sm:border sm:bg-card sm:shadow">
          <CardContent className="p-6 sm:p-6 md:p-8 text-center space-y-3">
            {(loading || status === "loading" || status === "unauthenticated") && <Spinner />}

            {!(loading || status !== "authenticated") && success === true && (
              <p>
                Your email has been changed to <strong>{email}</strong>!
              </p>
            )}
            {!(loading || status !== "authenticated") && success === false && (
              <Alert variant="destructive">
                <AlertDescription>
                  Error, invalid or expired email change token!
                  {errorMessage && (
                    <>
                      <br />
                      <span className="text-xs opacity-80">{errorMessage}</span>
                    </>
                  )}
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
