// components/TrackingHeader.tsx
import { TrackingStatus } from "@karrio/types/rest/api";
import { TrackerStatusEnum, TrackerType } from "@karrio/types";
import { formatDayDate, formatRef, isNone } from "@karrio/lib";
import { CarrierImage } from "@karrio/ui/components/carrier-image";

const TrackingHeader: React.FC<{ tracker: TrackingStatus }> = ({ tracker }) => {
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
          <p className="has-text-weight-bold my-4 is-size-6">
            Additional Information
          </p>
          <div className="columns is-multiline">
            {Object.entries(tracker.info)
              .filter(([_, value]) => value != null) // Exclude null or undefined values
              .map(([key, value], index) => (
                <div key={index} className="column is-6">
                  <strong>{key}: </strong> <span>{String(value)}</span>
                </div>
              ))}
          </div>
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
