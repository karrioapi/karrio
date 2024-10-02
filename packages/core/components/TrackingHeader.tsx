// components/TrackingHeader.tsx
"use client";

import { useState } from "react";
import { TrackerStatusEnum, TrackerType } from "@karrio/types";
import { formatDayDate, formatRef, isNone } from "@karrio/lib";
import { CarrierImage } from "@karrio/ui/components/carrier-image";

const TrackingHeader: React.FC<{ tracker: TrackerType }> = ({ tracker }) => {
  const [isExpanded, setIsExpanded] = useState(false); // State to control expansion

  const computeColor = (tracker: TrackerType) => {
    if (tracker?.delivered) return "has-background-success";
    else if (tracker?.status === TrackerStatusEnum.pending.toString())
      return "has-background-grey-dark";
    else if (
      [
        TrackerStatusEnum.on_hold.toString(),
        TrackerStatusEnum.delivery_delayed.toString(),
      ].includes(tracker?.status as string)
    )
      return "has-background-warning";
    else if (
      [TrackerStatusEnum.unknown.toString()].includes(
        tracker?.status as string,
      )
    )
      return "has-background-grey";
    else if (
      [TrackerStatusEnum.delivery_failed.toString()].includes(
        tracker?.status as string,
      )
    )
      return "has-background-danger";
    else return "has-background-info";
  };

  const computeStatus = (tracker: TrackerType) => {
    if (tracker?.delivered) return "Delivered";
    else if (tracker?.status === TrackerStatusEnum.pending.toString())
      return "Pending";
    else if (
      [
        TrackerStatusEnum.on_hold.toString(),
        TrackerStatusEnum.delivery_delayed.toString(),
        TrackerStatusEnum.ready_for_pickup.toString(),
        TrackerStatusEnum.unknown.toString(),
        TrackerStatusEnum.delivery_failed.toString(),
      ].includes(tracker?.status as string)
    )
      return formatRef(tracker!.status as string);
    else return "In-Transit";
  };

  const prettifyKey = (key: string) => {
    // Convert snake_case to "Pretty Case"
    return key
      .replace(/_/g, " ") // Replace underscores with spaces
      .replace(/\b\w/g, (char) => char.toUpperCase()); // Capitalize each word
  };

  const customRender = (key: string, value: any) => {
    switch (key) {
      case "carrier_tracking_link":
        return (
          <a href={String(value)} target="_blank" rel="noopener noreferrer">
            {String(value)}
          </a>
        );
      // Add more cases as needed for custom rendering of specific fields
      default:
        return <span>{String(value)}</span>;
    }
  };

  return (
    <>
      <div className="pb-4 is-flex is-justify-content-center">
        <CarrierImage
          carrier_name={tracker.carrier_name}
          width={60}
          height={60}
        />
      </div>

      <p className="subtitle has-text-centered is-6 my-3">
        <span>Tracking ID</span> <strong>{tracker.tracking_number}</strong>
      </p>

      {!isNone(tracker?.estimated_delivery) && (
        <p className="subtitle has-text-centered is-6 mb-3">
          <span>{tracker?.delivered ? "Delivered" : "Estimated Delivery"}</span>{" "}
          <strong>
            {formatDayDate(tracker!.estimated_delivery as string)}
          </strong>
        </p>
      )}

      {!isNone(tracker?.info) && (
        <>
          <hr />
          {/* Accessible button to toggle section */}
          <button
            onClick={() => setIsExpanded(!isExpanded)}
            aria-expanded={isExpanded} // Accessibility: indicate expanded state
            aria-controls="additional-info" // Accessibility: points to content
            className="has-text-weight-bold my-4 is-size-6 is-flex is-align-items-center"
            style={{ cursor: "pointer", background: "none", border: "none" }}
          >
            <span>{isExpanded ? "-" : "+"}</span>
            <span className="ml-2">Additional Information</span>
          </button>

          {/* Conditionally render additional info */}
          {isExpanded && (
            <div id="additional-info" className="columns is-multiline">
              {Object.entries(tracker.info || {})
                .filter(([_, value]) => value != null) // Exclude null or undefined values
                .map(([key, value], index) => (
                  <div key={index} className="column is-6">
                    <strong>{prettifyKey(key)}: </strong>{" "}
                    {customRender(key, value)}
                  </div>
                ))}
            </div>
          )}
        </>
      )}

      <p
        className={
          computeColor(tracker as TrackerType) +
          " block has-text-centered has-text-white is-size-4 py-3"
        }
      >
        {computeStatus(tracker as TrackerType)}
      </p>
    </>
  );
};

export default TrackingHeader;
