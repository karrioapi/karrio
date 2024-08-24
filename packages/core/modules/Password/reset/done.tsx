"use client";
import { dynamicMetadata } from "@karrio/core/components/metadata";
import Link from "next/link";
import React from "react";

export const generateMetadata = dynamicMetadata("Password Reset Complete");

export default function Page(pageProps: any) {
  return (
    <>
      <div className="card isolated-card my-6">
        <div className="card-content has-text-centered">
          <p className="subtitle mb-4">Password Reset Complete</p>

          <p>Your password has been set.</p>
          <p>You may go ahead and log in now.</p>
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
