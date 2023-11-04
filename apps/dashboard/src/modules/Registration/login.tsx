import { useAPIMetadata } from "@/context/api-metadata";
import SectionLayout from "@/layouts/section-layout";
import { useRouter } from "next/dist/client/router";
import { getCookie, isNone } from "@/lib/helper";
import React, { FormEvent, useRef } from "react";
import { signIn } from "next-auth/react";
import { p } from "@/lib/client";
import Head from "next/head";
import Link from "next/link";

export { getServerSideProps } from '@/lib/data-fetching/metadata';


export default function LoginPage(pageProps: any) {
  const router = useRouter();
  const { references } = useAPIMetadata();
  const email = useRef<HTMLInputElement>(null);
  const password = useRef<HTMLInputElement>(null);
  const [showError, setShowError] = React.useState<boolean>(false);
  const [isLoading, setIsLoading] = React.useState<boolean>(false);

  const onSubmit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setShowError(false);
    setIsLoading(true);

    const orgId = getCookie('orgId');
    const response: any = await signIn('credentials', {
      redirect: false,
      email: email.current?.value,
      password: password.current?.value,
      ...(!!orgId ? { orgId } : {}),
    });

    if (response.ok) {
      setTimeout(() => window.location.replace(p`${(new URLSearchParams(location.search)).get('next') || '/'}`), 500);
    } else {
      setShowError(true);
      setTimeout(() => setIsLoading(false), 1000);
    }
  };

  return (
    <>
      <SectionLayout {...pageProps}>
        <Head><title>{`Login - ${references.APP_NAME}`}</title></Head>

        <div className="card isolated-card">
          <div className="card-content">
            <p className="subtitle has-text-centered">Sign in to your account</p>

            {showError && <p className="has-text-danger is-size-6 has-text-centered">
              Please enter a correct email address and password. <br />
              Note that both fields may be case-sensitive.
            </p>}

            <form method="post" onSubmit={onSubmit}>

              <div className="field mt-6">
                <label className="label" htmlFor="id_email">Email</label>
                <div className="control">
                  <input
                    className="input"
                    id="id_email"
                    name="email"
                    type="email"
                    placeholder="Email"
                    value={"" || router.query.email}
                    disabled={!isNone(router.query.email)}
                    ref={email}
                    required
                  />
                </div>
              </div>

              <div className="field mt-5">
                <label className="label level" htmlFor="id_password">
                  <span>Password</span>
                  <Link legacyBehavior href="/password/reset/request" passHref><a className="is-size-7" tabIndex={-1}>Forgot your password?</a></Link>
                </label>

                <div className="control">
                  <input className="input" id="id_password" name="password" type="password" placeholder="Password" required ref={password} />
                </div>
              </div>

              <div className="field mt-6">
                <div className="control">
                  <input
                    disabled={isLoading}
                    className={"button is-primary is-fullwidth"}
                    type="submit"
                    value="Log in"
                  />
                </div>
              </div>

            </form>
          </div>
        </div>

        {pageProps?.metadata?.ALLOW_SIGNUP && <div className="has-text-centered my-4 is-size-6">
          Dont have an account? <Link legacyBehavior href="/signup" passHref><a>Sign Up</a></Link>
        </div>}
      </SectionLayout>
    </>
  )
}
