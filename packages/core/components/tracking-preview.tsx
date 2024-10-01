import {
  formatAddressRegion,
  formatRef,
  isNone,
} from "@karrio/lib";
import {
  TrackerType,
} from "@karrio/types";
import { AppLink } from "@karrio/ui/components/app-link";
import React, { useRef, useState } from "react";
import { useLocation } from "@karrio/hooks/location";
import TrackingHeader from "./TrackingHeader";
import TrackingEvents from "./TrackingEvents";
import TrackingMessages from "./TrackingMessages";

type TrackingPreviewContextType = {
  previewTracker: (tracker: TrackerType) => void;
};

interface TrackingPreviewComponent {
  children?: React.ReactNode;
}

export const TrackingPreviewContext =
  React.createContext<TrackingPreviewContextType>(
    {} as TrackingPreviewContextType,
  );

export const TrackingPreview: React.FC<TrackingPreviewComponent> = ({
  children,
}) => {
  const link = useRef<HTMLAnchorElement>(null);
  const { addUrlParam, removeUrlParam } = useLocation();
  const [isActive, setIsActive] = useState<boolean>(false);
  const [sharingLink, setSharingLink] = useState<string>("");
  const [key, setKey] = useState<string>(`tracker-${Date.now()}`);
  const [tracker, setTracker] = useState<TrackerType>();

  const previewTracker = (tracker: TrackerType) => {
    setTracker(tracker);
    setIsActive(true);
    setKey(`tracker-${Date.now()}`);
    link.current?.setAttribute("href", `/tracking/${tracker.id}`);
    setSharingLink(link.current?.href as string);
    addUrlParam("modal", tracker.id);
  };
  const dismiss = (_?: React.MouseEvent) => {
    setIsActive(false);
    setTracker(undefined);
    setKey(`tracker-${Date.now()}`);
    removeUrlParam("modal");
  };
  const copy = (_: React.MouseEvent) => {
    var input = document.createElement("input");
    input.setAttribute("value", sharingLink);
    document.body.appendChild(input);
    input.select();
    document.execCommand("copy");
    document.body.removeChild(input);
  };

  return (
    <>
      <TrackingPreviewContext.Provider value={{ previewTracker }}>
        {children}
      </TrackingPreviewContext.Provider>

      <div className={`modal ${isActive ? "is-active" : ""}`} key={key}>
        <a ref={link}></a>
        <div className="modal-background" onClick={dismiss}></div>

        {!isNone(tracker) && (
          <div className="modal-card">
            <section className="modal-card-body">
              <TrackingHeader tracker={tracker as TrackerType} />

              <hr />

              <div
                className="my-3 pl-3"
                style={{ maxHeight: "40vh", overflowY: "scroll" }}
              >
                <TrackingEvents tracker={tracker as TrackerType} />
              </div>

              <TrackingMessages messages={tracker?.messages || [] } />
              
              {!isNone(tracker?.shipment) && (
                <>
                  <hr />
                  <p className="has-text-weight-bold my-4 is-size-6">
                    Shipment details
                  </p>

                  <div className="columns my-0">
                    <div className="column is-3 is-size-7 py-1">
                      Origin/Destination
                    </div>
                    <div className="column is-size-7 has-text-weight-semibold py-1">
                      <span>
                        {formatAddressRegion(tracker?.shipment?.shipper as any)}
                      </span>
                      <i className="fa fa-arrow-right px-3"></i>
                      <span>
                        {formatAddressRegion(
                          tracker?.shipment?.recipient as any,
                        )}
                      </span>
                    </div>
                  </div>

                  <div className="columns my-0">
                    <div className="column is-3 is-size-7 py-1">Service</div>
                    <div className="column is-size-7 has-text-weight-semibold py-1">
                      {formatRef(
                        tracker?.info?.shipment_service ||
                          tracker?.shipment?.meta?.service_name ||
                          tracker?.shipment?.service,
                      )}
                    </div>
                  </div>

                  {tracker?.shipment?.reference && (
                    <div className="columns my-0">
                      <div className="column is-3 is-size-7 py-1">
                        Reference
                      </div>
                      <div className="column is-size-7 has-text-weight-semibold py-1">
                        {tracker?.shipment?.reference}
                      </div>
                    </div>
                  )}

                  <div className="columns my-0">
                    <div className="column is-3 is-size-7 py-1">Link</div>
                    <div className="column py-1">
                      <AppLink
                        className="has-text-info p-0 m-0 is-size-7 has-text-weight-semibold"
                        href={`/shipments/${tracker?.shipment?.id}`}
                        target="_blank"
                      >
                        <span>{tracker?.shipment?.id}</span>{" "}
                        <span style={{ fontSize: "0.7em" }}>
                          <i className="fas fa-external-link-alt"></i>
                        </span>
                      </AppLink>
                    </div>
                  </div>
                </>
              )}

              <hr />

              <div className="field">
                <div className="control">
                  <label className="label">Share</label>
                  <input
                    className="input is-small"
                    type="text"
                    title="Click to Copy"
                    value={sharingLink}
                    style={{ width: "80%" }}
                    readOnly
                  />
                  <button
                    className="button is-small is-light mx-1"
                    onClick={copy}
                  >
                    <span className="icon is-small">
                      <i className="fas fa-copy"></i>
                    </span>
                  </button>
                  <a
                    className="button is-small is-light"
                    href={sharingLink}
                    target="_blank"
                  >
                    <span className="icon is-small">
                      <i className="fas fa-share-square"></i>
                    </span>
                  </a>
                </div>
              </div>
            </section>
          </div>
        )}

        <button
          className="modal-close is-large has-background-dark"
          aria-label="close"
          onClick={dismiss}
        ></button>
      </div>
    </>
  );
};
