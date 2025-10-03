"use client";
import Link from "next/link";
import React from "react";
import { Card, CardContent } from "@karrio/ui/components/ui/card";
import { Button } from "@karrio/ui/components/ui/button";


export default function Page(pageProps: any) {
  return (
    <>
      <div className="px-4">
        <Card className="mx-auto mt-6 w-full max-w-md md:max-w-lg lg:max-w-xl border-0 bg-transparent shadow-none sm:border sm:bg-card sm:shadow">
          <CardContent className="p-6 sm:p-6 md:p-8 text-center space-y-3">
          <p className="text-lg font-medium">Password Reset Sent</p>
          <p>
            We’ve emailed you instructions for setting your password, if an
            account exists with the email you entered. You should receive them
            shortly.
          </p>
          <p className="text-sm text-muted-foreground">
            If you don’t receive an email, please make sure you’ve entered the
            address you registered with, and check your spam folder.
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
