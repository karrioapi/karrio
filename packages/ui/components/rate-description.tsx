import { formatRef, isNone } from "@karrio/lib";
import { RateType } from "@karrio/types";
import React from "react";

interface RateDescriptionComponent {
  rate: RateType;
}

export const RateDescription = ({
  rate,
}: RateDescriptionComponent): JSX.Element => {
  return (
    <div className="rate-description column px-2 py-1 is-size-7">
      <div className="rate-service has-text-weight-bold mb-1">
        {formatRef(
          ((rate.meta as any)?.service_name || rate.service) as string,
        )}
      </div>

      <div className="rate-details has-text-grey">
        <span className="rate-cost">
          {rate.total_charge} {rate.currency}
        </span>
        {!isNone(rate.transit_days) && (
          <span className="rate-transit">
            {" "}
            - {rate.transit_days} Transit days
          </span>
        )}
      </div>

      <div
        className="rate-carrier has-text-info"
        style={{ fontSize: "0.75rem" }}
      >
        {rate.carrier_name}:{rate.carrier_id}
      </div>

      <style jsx>{`
        .rate-description {
          min-width: 0; /* Enable flexbox text truncation */
          line-height: 1.2;
        }

        .rate-service,
        .rate-details,
        .rate-carrier {
          overflow: hidden;
          text-overflow: ellipsis;
          white-space: nowrap;
          width: 100%;
        }

        /* Apply minimum width for larger screens */
        @media screen and (min-width: 768px) {
          .rate-description {
            min-width: 190px;
          }
        }

        /* Allow wrapping on very small screens */
        @media screen and (max-width: 480px) {
          .rate-details {
            white-space: normal;
          }
        }
      `}</style>
    </div>
  );
};
