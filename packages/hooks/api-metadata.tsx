import { onError, url$, KARRIO_URL, MULTI_TENANT } from "@karrio/lib";
import { Metadata, References } from "@karrio/types";
import { useQuery } from "@tanstack/react-query";
import { useSyncedSession } from "./session";
import React, { useContext } from "react";
import axios from "axios";

type APIMeta = {
  host: string;
  metadata: Metadata;
  references: References;
};
const APIMetadata = React.createContext<APIMeta>({} as any);

const APIMetadataProvider: React.FC<{
  metadata: Metadata;
  children?: React.ReactNode;
}> = ({ children, metadata }) => {
  const {
    query: { data: session },
  } = useSyncedSession();
  const context = {
    metadata: (metadata || {}) as Metadata,
    get host() {
      return (
        MULTI_TENANT ? metadata?.HOST || KARRIO_URL : KARRIO_URL
      ) as string;
    },
  };

  const { data: references } = useQuery({
    queryKey: ["references", session?.accessToken],
    queryFn: () =>
      axios
        .get<References>(
          url$`${context.host}/v1/references?reduced=false`,
          !!session?.accessToken
            ? {
                headers: { authorization: `Bearer ${session?.accessToken}` },
              }
            : {},
        )
        .then(({ data }) => data),
    refetchOnWindowFocus: false,
    staleTime: 300000,
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
};

export function useAPIMetadata() {
  return useContext(APIMetadata);
}

export default APIMetadataProvider;
