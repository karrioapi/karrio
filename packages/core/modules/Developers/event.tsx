"use client";
import { formatDateTimeLong, isNone, notEmptyJSON } from "@karrio/lib";
import { dynamicMetadata } from "@karrio/core/components/metadata";
import { CopiableLink } from "@karrio/ui/components/copiable-link";
import { useLoader } from "@karrio/ui/components/loader";
import { AppLink } from "@karrio/ui/components/app-link";
import json from "highlight.js/lib/languages/json";
import React, { useEffect, useState } from "react";
import { useEvent } from "@karrio/hooks/event";
import hljs from "highlight.js";

export const generateMetadata = dynamicMetadata("Event");
hljs.registerLanguage("json", json);

export const EventComponent: React.FC<{
  eventId: string;
  isPreview?: boolean;
}> = ({ eventId, isPreview }) => {
  const { setLoading } = useLoader();
  const entity_id = eventId;
  const [data, setData] = useState<string>();
  const {
    query: { data: { event } = {}, ...query },
  } = useEvent(entity_id);

  useEffect(() => {
    setLoading(query.isFetching);
  }, [query.isFetching]);
  useEffect(() => {
    if (event !== undefined) {
      setData(JSON.stringify(event || {}, null, 2));
    }
  });

  return (
    <>
      {!isNone(event?.id) && (
        <>
          <div className="columns my-1">
            <div className="column is-6">
              <span className="subtitle is-size-7 has-text-weight-semibold">
                EVENT
              </span>
              <br />
              <span className="title is-4 mr-2">{event?.type}</span>
            </div>

            <div className="column is-6 pb-0">
              <p className="has-text-right">
                <CopiableLink text={event?.id as string} title="Copy ID" />
              </p>
              {isPreview && (
                <p className="has-text-right">
                  <AppLink
                    href={`/developers/events/${eventId}`}
                    target="_blank"
                    className="button is-default has-text-info is-small mx-1"
                  >
                    <span className="icon">
                      <i className="fas fa-external-link-alt"></i>
                    </span>
                  </AppLink>
                </p>
              )}
            </div>
          </div>

          <hr className="mt-1 mb-2" style={{ height: "1px" }} />

          <div className="columns mb-4">
            <div className="p-4 mr-4">
              <span className="subtitle is-size-7 my-4">Date</span>
              <br />
              <span className="subtitle is-size-7 has-text-weight-semibold">
                {formatDateTimeLong(event?.created_at)}
              </span>
            </div>

            <div
              className="my-2"
              style={{ width: "1px", backgroundColor: "#ddd" }}
            ></div>

            <div className="p-4 mr-4">
              <span className="subtitle is-size-7 my-4">Source</span>
              <br />
              <span className="subtitle is-size-7 has-text-weight-semibold">
                Automatic
              </span>
            </div>
          </div>

          <h2 className="title is-5 my-4">Event data</h2>
          <hr className="mt-1 mb-2" style={{ height: "1px" }} />

          {notEmptyJSON(data) && (
            <div className="py-3 is-relative">
              <CopiableLink
                text="COPY"
                value={data}
                style={{ position: "absolute", right: 0, zIndex: 1 }}
                className="button is-primary is-small m-1"
              />
              <pre className="code p-1">
                <code
                  dangerouslySetInnerHTML={{
                    __html: hljs.highlight(data as string, { language: "json" })
                      .value,
                  }}
                />
              </pre>
            </div>
          )}
        </>
      )}
    </>
  );
};

export default function EventPage({ params }: { params: { id: string } }) {
  return (
    <>
      <EventComponent eventId={params.id} />
    </>
  );
}
