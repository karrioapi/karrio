import { loadAPIMetadata, checkSubscription, createPortalSession } from "@/lib/data-fetching";
import { Metadata, SubscriptionType } from "@/lib/types";
import { GetServerSideProps, NextPage } from "next";
import { getSession } from "next-auth/react";
import { isNone } from "@/lib/helper";
import { p } from "@/lib/client";
import Head from "next/head";
import React from "react";

type BillingPageProps = { metadata: Metadata, subscription?: SubscriptionType, session_url?: string };

const Billing: NextPage<BillingPageProps> = ({ metadata, subscription, session_url }) => {
  return (
    <>
      <Head><title>{`Billing - ${metadata?.APP_NAME}`}</title></Head>

      <section className="hero is-fullheight p-2">

        <div className="container">

          <div className="has-text-centered my-4">
            <a href={p`/login`} className="is-size-4 has-text-primary has-text-weight-bold is-lowercase">
              {metadata.APP_NAME}
            </a>
          </div>

          {!subscription?.is_owner && <div className="card isolated-card my-6">
            <div className="card-content has-text-centered ">
              <p>Your subscription has expired.</p>
              <p>Please notify your account admnistrator.</p>
            </div>
          </div>}

          {subscription?.is_owner && <div className="card isolated-card my-6">
            <div className="card-content">

              <p className="subtitle has-text-centered mb-4">Billing Setup</p>
              <p className="has-text-centered mb-4">Update your billing and subscription on Stripe.</p>

              <a className="button is-primary is-fullwidth mt-6" href={session_url}>
                <span>Open Customer Portal</span>
              </a>

            </div>
          </div>}

        </div>

      </section >
    </>
  )
};

export const getServerSideProps: GetServerSideProps = async (ctx) => {
  const session = await getSession(ctx);

  if (isNone((session as any)?.accessToken)) {
    return {
      redirect: {
        permanent: false,
        destination: '/login'
      }
    }
  }

  const metadata = await loadAPIMetadata(ctx).catch(_ => _);
  const subscription = await checkSubscription(session, metadata.metadata).catch(_ => _);
  const portal_session = await createPortalSession(
    session,
    ctx.req.headers.host as string,
    subscription.subscription,
    metadata.metadata,
  );

  return { props: { ...metadata, ...subscription, ...portal_session } };
};

export default Billing;
