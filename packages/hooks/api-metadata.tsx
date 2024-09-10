"use client";

import { Metadata, References } from "@karrio/types";
import { useQuery } from "@tanstack/react-query";
import { useSyncedSession } from "./session";
import { onError, url$ } from "@karrio/lib";
import React, { useContext } from "react";
import axios from "axios";

type APIMeta = {
  metadata: Metadata;
  references: References;
  getHost: () => string;
};
const APIMetadata = React.createContext<APIMeta>({} as any);

function APIMetadataProvider({
  children,
  metadata,
  MULTI_TENANT,
  KARRIO_PUBLIC_URL,
}: {
  metadata: Metadata;
  MULTI_TENANT?: boolean;
  KARRIO_PUBLIC_URL?: string;
  children?: React.ReactNode;
}) {
  const {
    query: { data: session },
  } = useSyncedSession();
  const getHost = () =>
    (MULTI_TENANT
      ? metadata?.HOST || KARRIO_PUBLIC_URL
      : KARRIO_PUBLIC_URL) as string;
  const context = {
    getHost,
    metadata: (metadata || {}) as Metadata,
  };

  const { data: references } = useQuery({
    queryKey: ["references", session?.accessToken],
    queryFn: () =>
      axios
        .get<References>(
          url$`${getHost()}/v1/references?reduced=false`,
          !!session?.accessToken
            ? {
                headers: { authorization: `Bearer ${session?.accessToken}` },
              }
            : {},
        )
        .then(({ data }) => data),
    refetchOnWindowFocus: false,
    staleTime: 300000,
    enabled: !!getHost(),
    onError,
  });

  return (
    <APIMetadata.Provider
      value={{
        ...context,
        references: (references || metadata || {}) as References,
      }}
    >
      {children}
    </APIMetadata.Provider>
  );
}

export function useAPIMetadata() {
  return useContext(APIMetadata);
}

export default APIMetadataProvider;
