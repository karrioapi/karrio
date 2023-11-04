import { formatDateTimeLong, isNone, notEmptyJSON } from "@/lib/helper";
import AuthenticatedPage from "@/layouts/authenticated-page";
import DashboardLayout from "@/layouts/dashboard-layout";
import CopiableLink from "@/components/copiable-link";
import { useRouter } from "next/dist/client/router";
import json from 'highlight.js/lib/languages/json';
import React, { useEffect, useState } from "react";
import { useLoader } from "@/components/loader";
import AppLink from "@/components/app-link";
import { useEvent } from "@/context/event";
import hljs from "highlight.js";
import Head from "next/head";

export { getServerSideProps } from "@/lib/data-fetching";

hljs.registerLanguage('json', json);


export const EventComponent: React.FC<{ eventId?: string }> = ({ eventId }) => {
  const router = useRouter();
  const { setLoading } = useLoader();
  const entity_id = eventId || router.query.id as string;
  const [data, setData] = useState<string>();
  const { query: { data: { event } = {}, ...query } } = useEvent(entity_id);

  useEffect(() => { setLoading(query.isFetching); }, [query.isFetching]);
  useEffect(() => {
    if (event !== undefined) {
      setData(JSON.stringify(event || {}, null, 2));
    }
  });

  return (
    <>
      {!isNone(event?.id) && <>

        <div className="columns my-1">
          <div className="column is-6">
            <span className="subtitle is-size-7 has-text-weight-semibold">EVENT</span>
            <br />
            <span className="title is-4 mr-2">{event?.type}</span>
          </div>

          <div className="column is-6 pb-0">
            <p className="has-text-right">
              <CopiableLink text={event?.id as string} title="Copy ID" />
            </p>
            {!isNone(eventId) && <p className="has-text-right">
              <AppLink
                href={`/developers/events/${eventId}`} target="blank"
                className="button is-default has-text-info is-small mx-1">
                <span className="icon">
                  <i className="fas fa-external-link-alt"></i>
                </span>
              </AppLink>
            </p>}
          </div>
        </div>

        <hr className="mt-1 mb-2" style={{ height: '1px' }} />

        <div className="columns mb-4">
          <div className="p-4 mr-4">
            <span className="subtitle is-size-7 my-4">Date</span><br />
            <span className="subtitle is-size-7 has-text-weight-semibold">{formatDateTimeLong(event?.created_at)}</span>
          </div>

          <div className="my-2" style={{ width: '1px', backgroundColor: '#ddd' }}></div>

          <div className="p-4 mr-4">
            <span className="subtitle is-size-7 my-4">Source</span><br />
            <span className="subtitle is-size-7 has-text-weight-semibold">Automatic</span>
          </div>
        </div>

        <h2 className="title is-5 my-4">Event data</h2>
        <hr className="mt-1 mb-2" style={{ height: '1px' }} />

        {notEmptyJSON(data) &&
          <div className="py-3 is-relative">
            <CopiableLink text="COPY"
              value={data}
              style={{ position: 'absolute', right: 0, zIndex: 1 }}
              className="button is-primary is-small m-1"
            />
            <pre className="code p-1">
              <code
                dangerouslySetInnerHTML={{
                  __html: hljs.highlight(data as string, { language: 'json' }).value,
                }}
              />
            </pre>
          </div>}

      </>}
    </>
  );
};


export default function EventPage(pageProps: any) {
  return AuthenticatedPage((
    <DashboardLayout>
      <Head><title>{`Event - ${(pageProps as any).metadata?.APP_NAME}`}</title></Head>
      <EventComponent />
    </DashboardLayout>
  ), pageProps);
}
