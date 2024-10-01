import { TrackingStatus } from "@karrio/types/rest/api";
import TrackingHeader from "@/components/TrackingHeader";
import TrackingEvents from "@/components/TrackingEvents";
import TrackingMessages from "@/components/TrackingMessages";
import { isNone } from "@karrio/lib";
import { Metadata, TrackerType } from "@karrio/types";
import { NextPage } from "next";
import Head from "next/head";
import Link from "next/link";
import React from "react";

export { getServerSideProps } from "@/context/tracker";

const Tracking: NextPage<{
  id: string;
  metadata: Metadata;
  tracker?: TrackingStatus;
  message?: string;
}> = ({ metadata, id, tracker, message }) => {
  // Normalize messages to replace undefined with null for TypeScript compatibility
  const normalizedMessages = (tracker?.messages || []).map((message) => ({
    ...message,
    carrier_name: message.carrier_name ?? null, // Convert undefined to null
    carrier_id: message.carrier_id ?? null, // Convert undefined to null
    message: message.message ?? null,
    code: message.code ?? null,
    details: message.details ?? null,
  }));

  return (
    <>
      <Head>
        <title>{`Tracking - ${tracker?.tracking_number || id} - ${metadata?.APP_NAME}`}</title>
      </Head>

      <section className="hero is-fullheight p-2">

        <div className="container">

          <div className="has-text-centered my-4">
            <Link legacyBehavior href="/">
              <span className="is-size-4 has-text-primary has-text-weight-bold is-lowercase">
                {metadata?.APP_NAME}
              </span>
            </Link>
          </div>

          {!isNone(tracker) && (
            <>
              <div className="card isolated-card">
                <div className="card-content">
                  <TrackingHeader tracker={tracker as TrackerType} />
                </div>
                <footer className="card-footer"></footer>
              </div>
              <hr />
              <TrackingEvents tracker={tracker as TrackerType} />
            </>
          )}

          {/* Pass normalized messages to the component */}
          <TrackingMessages messages={normalizedMessages} />

          {!isNone(message) && (
            <div className="card isolated-card my-6">
              <div className="card-content has-text-centered ">
                <p>{message}</p>
              </div>
            </div>
          )}
        </div>
        <hr className="mt-4" />

        <div className="hero-footer mb-4">
          <div className="content has-text-centered">
            <p>
              <Link legacyBehavior href="/" className="button is-white">
                <span>Powered by &copy; {metadata.APP_NAME}</span>
              </Link>
            </p>
          </div>
        </div>
      </section>
    </>
  );
};

export default Tracking;
