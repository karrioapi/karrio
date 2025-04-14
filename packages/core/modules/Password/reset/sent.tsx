"use client";
import Link from "next/link";
import React from "react";


export default function Page(pageProps: any) {
  return (
    <>
      <div className="card isolated-card my-6">
        <div className="card-content has-text-centered">
          <p className="subtitle mb-4">Password Reset Sent</p>

          <p>
            We’ve emailed you instructions for setting your password, if an
            account exists with the email you entered. You should receive them
            shortly.
          </p>
          <p className="is-size-6 has-text-weight-light pt-2">
            If you don’t receive an email, please make sure you’ve entered the
            address you registered with, and check your spam folder.
          </p>
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
