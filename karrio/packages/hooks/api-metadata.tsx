"use client";

import { Metadata, References } from "@karrio/types";
import { useAuthenticatedQuery } from "./karrio";
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

  const getHost = () => {
    const host = (MULTI_TENANT
      ? metadata?.HOST || KARRIO_PUBLIC_URL
      : KARRIO_PUBLIC_URL) as string;

    return host;
  };

  const context = {
    getHost,
    metadata: (metadata || {}) as Metadata,
  };

  const host = getHost();
  const isEnabled = !!host && host !== 'undefined';

  const { data: references, isLoading, error } = useAuthenticatedQuery({
    queryKey: ["references", session?.accessToken, host],
    queryFn: () => {
      return axios
        .get<References>(
          url$`${host}/v1/references?reduced=false`,
          !!session?.accessToken
            ? {
              headers: { authorization: `Bearer ${session?.accessToken}` },
            }
            : {},
        )
        .then(({ data }) => {
          return data;
        })
        .catch((err) => {
          throw err;
        });
    },
    refetchOnWindowFocus: false,
    staleTime: 300000,
    enabled: isEnabled,
    requireAuth: false,
    onError: (err) => {
      onError(err);
    },
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
