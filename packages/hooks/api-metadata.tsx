"use client";

import { Metadata, References } from "@karrio/types";
import { useAuthenticatedQuery } from "./karrio";
import { useSyncedSession } from "./session";
import { onError, url$ } from "@karrio/lib";
import React, { useContext, useMemo } from "react";
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
    // Auto-refresh to reflect admin config changes without manual reload
    refetchOnWindowFocus: true,
    refetchOnReconnect: true,
    staleTime: 0,
    enabled: isEnabled,
    requireAuth: false,
    onError: (err) => {
      onError(err);
    },
  });

  // Merge live feature flags from references into metadata so UI reflects changes without full
  // page reload. Only override known flag keys to keep metadata shape stable.
  const mergedMetadata = useMemo(() => {
    const base = (metadata || {}) as any;
    const src = (references || {}) as any;
    const flagKeys = [
      "AUDIT_LOGGING",
      "ALLOW_SIGNUP",
      "ALLOW_ADMIN_APPROVED_SIGNUP",
      "ALLOW_MULTI_ACCOUNT",
      "ADMIN_DASHBOARD",
      "MULTI_ORGANIZATIONS",
      "ORDERS_MANAGEMENT",
      "APPS_MANAGEMENT",
      "DOCUMENTS_MANAGEMENT",
      "DATA_IMPORT_EXPORT",
      "PERSIST_SDK_TRACING",
      "WORKFLOW_MANAGEMENT",
      "SHIPPING_RULES",
      "ADVANCED_ANALYTICS",
    ];
    const overlay: Record<string, any> = {};
    flagKeys.forEach((k) => {
      if (typeof src?.[k] !== "undefined") overlay[k] = src[k];
    });
    return { ...(base || {}), ...overlay } as Metadata;
  }, [references, metadata]);

  return (
    <APIMetadata.Provider
      value={{
        ...context,
        metadata: mergedMetadata,
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
