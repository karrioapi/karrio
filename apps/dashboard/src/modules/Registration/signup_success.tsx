import SectionLayout from "@/layouts/section-layout";
import Head from "next/head";
import Link from "next/link";
import React from "react";

export { getServerSideProps } from '@/lib/data-fetching/metadata';


function SignUpSuccess(pageProps: any) {
  return (
    <>
      <SectionLayout {...pageProps}>
        <Head><title>{`Sign Up Success - ${pageProps.metadata?.APP_NAME}`}</title></Head>

        <div className="card isolated-card my-6">
          <div className="card-content has-text-centered ">

            <p>Your account has been created.</p>
            <p>Check your registration email inbox to verify the address and activate your account.</p>

          </div>
        </div>

        <div className="has-text-centered my-4 is-size-6">
          <Link legacyBehavior href="/login">Sign in</Link>
        </div>

      </SectionLayout>
    </>
  )
};


export default SignUpSuccess;
