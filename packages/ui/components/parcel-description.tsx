import {
  formatParcelLabel,
  formatDimension,
  formatWeight,
  isNoneOrEmpty,
} from "@karrio/lib";
import { ParcelType } from "@karrio/types";
import React from "react";

interface ParcelDescriptionComponent {
  parcel?: ParcelType;
  suffix?: React.ReactNode | string;
  prefix?: React.ReactNode | string;
}

export const ParcelDescription = ({
  parcel,
  prefix,
  suffix,
}: ParcelDescriptionComponent): JSX.Element => {
  const weightDescription = formatWeight(parcel);
  const dimensionDescription = formatDimension(parcel);

  return (
    <>
      <p className="text-xs my-1 font-semibold text-ellipsis">
        {prefix} {formatParcelLabel(parcel)} {suffix}
      </p>
      <p className="text-xs my-1 text-ellipsis">
        {dimensionDescription}
        {isNoneOrEmpty(dimensionDescription) || isNoneOrEmpty(weightDescription)
          ? ""
          : ", "}
        {weightDescription}
      </p>
      <p className="text-xs my-1 font-semibold text-muted-foreground text-ellipsis">
        {parcel?.description}
      </p>
    </>
  );
};