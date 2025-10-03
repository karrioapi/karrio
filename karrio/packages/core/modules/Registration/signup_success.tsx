"use client";
import React from "react";
import Link from "next/link";
import { Card, CardContent } from "@karrio/ui/components/ui/card";
import { Button } from "@karrio/ui/components/ui/button";

function SignUpSuccess(pageProps: any) {
  return (
    <>
      <div className="px-4">
        <Card className="mx-auto mt-6 w-full max-w-md md:max-w-lg lg:max-w-xl border-0 bg-transparent shadow-none sm:border sm:bg-card sm:shadow">
          <CardContent className="p-6 sm:p-6 md:p-8 text-center space-y-3">
            <p className="text-lg font-medium">Your account has been created.</p>
            <p className="text-sm text-muted-foreground">
              Check your registration email inbox to verify the address and activate your account.
            </p>
          </CardContent>
        </Card>
      </div>

      <div className="my-4 text-center">
        <Link href="/signin" className="inline-block">
          <Button>Sign in</Button>
        </Link>
      </div>
    </>
  );
}

export default SignUpSuccess;
