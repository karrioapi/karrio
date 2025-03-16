import { useAPIMetadata } from "@karrio/hooks/api-metadata";
import { formatCarrierSlug } from "@karrio/lib";
import React from "react";

interface AppBadgeComponent extends React.AllHTMLAttributes<HTMLSpanElement> {}

export const AppBadge = ({
  className,
  ...props
}: AppBadgeComponent): JSX.Element => {
  const {
    metadata: { APP_NAME },
  } = useAPIMetadata();

  return (
    <strong
      className={`is-lowercase has-text-weight-bold has-text-primary`}
      style={{ fontSize: "90%", borderRadius: "4px" }}
      {...props}
    >
      {formatCarrierSlug(APP_NAME)}
    </strong>
  );
};
