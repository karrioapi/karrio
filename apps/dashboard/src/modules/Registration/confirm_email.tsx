import { SectionLayout } from "@/layouts/section-layout";
import { Spinner } from "@karrio/ui/components/spinner";
import { useUserMutation } from "@karrio/hooks/user";
import { useRouter } from "next/dist/client/router";
import React, { useEffect } from "react";
import { isNone } from "@karrio/lib";
import Head from "next/head";
import Link from "next/link";

export { getServerSideProps } from '@/context/metadata';


export default function Page(pageProps: any) {
  const router = useRouter();
  const { token } = router.query as { token: string };
  const { confirmEmail: { isLoading, data, mutateAsync } } = useUserMutation();

  useEffect(() => { !isNone(token) && mutateAsync({ token }) }, [token]);

  return (
    <>
      <SectionLayout {...pageProps}>
        <Head><title>{`Sign Up Confirmation - ${pageProps.metadata?.APP_NAME}`}</title></Head>

        <div className="card isolated-card my-6">
          <div className="card-content has-text-centered ">

            {isLoading && <Spinner />}

            {(data?.confirm_email?.success === true) &&
              <p>Your account is verified!</p>}

            {(!isLoading && !data?.confirm_email?.success) &&
              <p>Error, invalid or expired account activation token!</p>}

          </div>
        </div>

        <div className="has-text-centered my-4 is-size-6">
          <Link legacyBehavior href="/login">Sign in</Link>
        </div>

      </SectionLayout>
    </>
  )
}
