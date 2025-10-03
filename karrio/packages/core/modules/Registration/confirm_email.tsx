"use client";
import React, { useEffect, useMemo } from "react";
import Link from "next/link";
import { usePathname, useSearchParams } from "next/navigation";
import { useUserMutation } from "@karrio/hooks/user";
import { isNone } from "@karrio/lib";
import { Spinner } from "@karrio/ui/core/components/spinner";
import { Card, CardContent } from "@karrio/ui/components/ui/card";
import { Alert, AlertDescription } from "@karrio/ui/components/ui/alert";


export default function Page(pageProps: any) {
  const searchParams = useSearchParams();
  const pathname = usePathname();
  // Support both /email?token=... and /email/<token>
  const token: string | null = useMemo(() => {
    const qp = searchParams.get("token");
    if (qp) return qp as string;
    const parts = (pathname || "").split("/").filter(Boolean);
    const idx = parts.indexOf("email");
    const seg = idx >= 0 && parts[idx + 1] ? parts[idx + 1] : parts[parts.length - 1];
    return seg && seg !== "email" ? seg : null;
  }, [searchParams, pathname]);
  const {
    confirmEmail: { isLoading, data, mutateAsync },
  } = useUserMutation();

  useEffect(() => {
    if (!isNone(token)) {
      mutateAsync({ token: token as string });
    }
  }, [token, mutateAsync]);

  return (
    <>
      <div className="px-4">
        <Card className="mx-auto mt-6 w-full max-w-md md:max-w-lg lg:max-w-xl border-0 bg-transparent shadow-none sm:border sm:bg-card sm:shadow">
          <CardContent className="p-6 sm:p-6 md:p-8 text-center space-y-3">
          {isLoading && <Spinner />}

          {data?.confirm_email?.success === true && (
            <p className="text-lg font-medium">Your account is verified!</p>
          )}

          {!isLoading && !data?.confirm_email?.success && (
            <Alert variant="destructive">
              <AlertDescription>
                Error, invalid or expired account activation token!
              </AlertDescription>
            </Alert>
          )}
          </CardContent>
        </Card>
      </div>

      <div className="my-4 text-center">
        <Link href="/signin" className="text-sm font-semibold text-primary hover:underline">
          Sign in
        </Link>
      </div>
    </>
  );
}
