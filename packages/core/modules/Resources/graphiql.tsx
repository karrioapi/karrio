"use client";
import React from "react";
import { useAPIMetadata } from "@karrio/hooks/api-metadata";
import { createGraphiQLFetcher } from "@graphiql/toolkit";
import { useSyncedSession } from "@karrio/hooks/session";
import { GraphiQL } from "graphiql";
import "graphiql/graphiql.min.css";

export default function GraphiQLPage() {
  const { metadata } = useAPIMetadata();
  const {
    query: { data: session },
  } = useSyncedSession();

  const fetcher = React.useMemo(() => {
    if (!metadata?.GRAPHQL) return null;

    return createGraphiQLFetcher({
      url: metadata.GRAPHQL,
      headers: {
        ...(session?.orgId ? { "x-org-id": session.orgId } : {}),
        ...(session?.testMode ? { "x-test-mode": session.testMode } : {}),
        ...(session?.accessToken
          ? { authorization: `Bearer ${session.accessToken}` }
          : {}),
      },
    });
  }, [metadata?.GRAPHQL, session?.accessToken, session?.orgId, session?.testMode]);

  if (!fetcher) {
    return <div className="p-4">Loading GraphQL Explorer...</div>;
  }

  return (
    <div
      className="playground-wrapper"
      style={{ position: "absolute", top: 0, left: 0, bottom: 0, right: 0 }}
    >
      <GraphiQL fetcher={fetcher as any} />
    </div>
  );
}
