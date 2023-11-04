import AuthenticatedPage from "@/layouts/authenticated-page";
import { useAPIMetadata } from "@/context/api-metadata";
import SectionLayout from "@/layouts/section-layout";
import { useRouter } from "next/dist/client/router";
import { useUserMutation } from "@/context/user";
import Spinner from "@/components/spinner";
import React, { useEffect } from "react";
import { isNone } from "@/lib/helper";
import Head from "next/head";
import Link from "next/link";

export { getServerSideProps } from '@/lib/data-fetching';


export default function Page(pageProps: any) {
  const { references } = useAPIMetadata();

  const Component: React.FC = () => {
    const router = useRouter();
    const { token } = router.query;
    const { confirmEmailChange } = useUserMutation();
    const [loading, setLoading] = React.useState(false);
    const [success, setSuccess] = React.useState(false);
    const [email, setEmail] = React.useState('');

    const confirm = async () => {
      setLoading(true);
      try {
        const { confirm_email_change } = await confirmEmailChange.mutateAsync({ token: token as string });
        const email = confirm_email_change.user?.email;
        setSuccess(!isNone(email));
        setEmail(email || '');
      } catch (e) {
        setSuccess(false);
      }
      setLoading(false);
    };

    useEffect(() => {
      if (!isNone(token)) {
        confirm();
      }
    }, [token]);

    return (
      <>
        <div className="card isolated-card my-6">
          <div className="card-content has-text-centered ">

            {loading && <Spinner />}

            {(!loading && success === true) && <p>Your email has been changed to <strong>{email}</strong>!</p>}
            {(!loading && success === false) && <p>Error, invalid or expired email change token!</p>}

          </div>
        </div>

        <div className="has-text-centered my-4 is-size-6">
          <Link legacyBehavior href="/">Return Home</Link>
        </div>
      </>
    );
  };

  return AuthenticatedPage((
    <SectionLayout {...pageProps}>
      <Head><title>{`Email change confirmation - ${references.APP_NAME}`}</title></Head>

      <Component />

    </SectionLayout>
  ), pageProps);
}
