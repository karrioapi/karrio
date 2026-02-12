import { Metadata, References } from "@karrio/types";
import { useKarrioEmbed } from "./karrio-embed-provider";
import React, { createContext, useContext } from "react";
import { useQuery } from "@tanstack/react-query";
import axios from "axios";

type APIMeta = {
  metadata: Metadata;
  references: References;
  getHost: () => string;
};

const APIMetadata = createContext<APIMeta>({} as APIMeta);

export function APIMetadataEmbedProvider({
  children,
}: {
  children: React.ReactNode;
}) {
  const { host, headers } = useKarrioEmbed();

  const { data: references, isLoading } = useQuery({
    queryKey: ["references", host],
    queryFn: () =>
      axios
        .get<References>(`${host}/v1/references?reduced=false`, { headers })
        .then(({ data }) => data),
    staleTime: 300000,
    enabled: !!host,
  });

  const getHost = () => host;

  if (isLoading || !references) {
    return (
      <div className="flex items-center justify-center h-screen">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary" />
      </div>
    );
  }

  return (
    <APIMetadata.Provider
      value={{
        metadata: references as unknown as Metadata,
        references,
        getHost,
      }}
    >
      {children}
    </APIMetadata.Provider>
  );
}

export function useAPIMetadata() {
  return useContext(APIMetadata);
}

export default APIMetadataEmbedProvider;
