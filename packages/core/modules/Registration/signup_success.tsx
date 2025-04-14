"use client";
import Link from "next/link";
import React from "react";


function SignUpSuccess(pageProps: any) {
  return (
    <>
      <div className="card isolated-card my-6">
        <div className="card-content has-text-centered ">
          <p>Your account has been created.</p>
          <p>
            Check your registration email inbox to verify the address and
            activate your account.
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

export default SignUpSuccess;
