import { TrackingEvent, TrackingStatus } from "@karrio/types/rest/api";
import TrackingHeader from "@/components/TrackingHeader";
import TrackingEvents from "@/components/TrackingEvents";
import TrackingMessages from "@/components/TrackingMessages";
import { formatDayDate, isNone } from "@karrio/lib";
import { Metadata } from "@karrio/types";
import { NextPage } from "next";
import Head from "next/head";
import Link from "next/link";
import React from "react";

export { getServerSideProps } from '@/context/tracker';

type DayEvents = { [k: string]: TrackingEvent[] };

const Tracking: NextPage<{ id: string, metadata: Metadata, tracker?: TrackingStatus, message?: string }> = ({ metadata, id, tracker, message }) => {

  const computeEvents = (tracker: TrackingStatus): DayEvents => {
    return (tracker?.events || []).reduce((days, event: TrackingEvent) => {
      const daydate = formatDayDate(event.date as string);
      return { ...days, [daydate]: [...(days[daydate] || []), event] };
    }, {} as DayEvents);
  };

  return (
    <>
      <Head><title>{`Tracking - ${tracker?.tracking_number || id} - ${metadata?.APP_NAME}`}</title></Head>

      <section className="hero is-fullheight p-2">

        <div className="container">

          <div className="has-text-centered my-4">
            <Link legacyBehavior href="/">
              <span className="is-size-4 has-text-primary has-text-weight-bold is-lowercase">{metadata?.APP_NAME}</span>
            </Link>
          </div>

          {!isNone(tracker) && <>
            <div className="card isolated-card">
              <div className="card-content">

                <TrackingHeader tracker={tracker as TrackingType} />

              </div>

              <footer className="card-footer">

              </footer>

            </div>

            <hr />

            <TrackingEvents tracker={tracker as TrackingType} />

          </>}

          <TrackingMessages messages={tracker?.messages} />

          {!isNone(message) && <div className="card isolated-card my-6">
            <div className="card-content has-text-centered ">
              <p>{message}</p>
            </div>
          </div>}

        </div >

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

      </section >
    </>
  )
};

export default Tracking;
