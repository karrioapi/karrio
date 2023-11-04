import { TrackingEvent, TrackingStatus } from "karrio/rest";
import CarrierImage from "@/components/carrier-image";
import { formatDayDate, isNone } from "@/lib/helper";
import { Metadata } from "@/lib/types";
import { NextPage } from "next";
import Head from "next/head";
import Link from "next/link";
import React from "react";

export { getServerSideProps } from '@/lib/data-fetching/tracker';

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

                <div className="pb-4 is-flex is-justify-content-center">
                  <CarrierImage carrier_name={tracker!.carrier_name} width={60} height={60} />
                </div>


                <p className="subtitle has-text-centered is-6 my-3">
                  <span>Tracking ID</span> <strong>{tracker?.tracking_number}</strong>
                </p>

                {!isNone(tracker?.estimated_delivery) && <p className="subtitle has-text-centered is-6 mb-3">
                  <span>{tracker?.delivered ? 'Delivered' : 'Estimated Delivery'}</span> {' '}
                  <strong>{formatDayDate(tracker!.estimated_delivery as string)}</strong>
                </p>}

              </div>

              <footer className="card-footer">

                {(tracker?.status === 'delivered') &&
                  <p className="card-footer-item has-background-success has-text-white is-size-4">Delivered</p>}

                {(tracker?.status === 'in_transit') &&
                  <p className="card-footer-item has-background-info has-text-white is-size-4">In-Transit</p>}

                {(tracker?.status !== 'delivered' && tracker?.status !== 'in_transit') &&
                  <p className="card-footer-item has-background-grey-dark has-text-white is-size-4">Pending</p>}

              </footer>

            </div>

            <hr />

            <div className="my-6">

              <aside className="menu">
                <ul className="menu-list mb-5" style={{ maxWidth: '28rem' }}>
                  {Object.entries(computeEvents(tracker as TrackingStatus)).map(([day, events], index) => <li key={index}>

                    <p className="menu-label is-size-6 is-capitalized">{day}</p>

                    {events.map((event, index) => <ul key={index}>
                      <li className="my-2">
                        <code>{event.time}</code>
                        <span className="is-subtitle is-size-7 my-1 has-text-weight-semibold">{event.location}</span>
                      </li>
                      <li className="my-2">
                        <span className="is-subtitle is-size-7 my-1 has-text-weight-semibold has-text-grey">{event.description}</span>
                      </li>
                    </ul>)}

                  </li>)}
                </ul>
              </aside>

            </div>

          </>}

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
