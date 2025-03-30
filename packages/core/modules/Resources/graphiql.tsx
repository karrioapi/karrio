"use client";
import { dynamicMetadata } from "@karrio/core/components/metadata";
import { useAPIMetadata } from "@karrio/hooks/api-metadata";
import { createGraphiQLFetcher } from "@graphiql/toolkit";
import { useSyncedSession } from "@karrio/hooks/session";
import {
  EditorContextProvider,
  ExecutionContextProvider,
  ExplorerContextProvider,
  HistoryContextProvider,
  SchemaContextProvider,
  StorageContextProvider,
  QueryEditor,
  ResponseEditor,
  VariableEditor,
  DocExplorer,
} from "@graphiql/react";
import "@graphiql/react/dist/style.css";
import React from "react";

export const generateMetadata = dynamicMetadata("GraphiQL");

export default function Page() {
  const { metadata } = useAPIMetadata();
  const {
    query: { data: session },
  } = useSyncedSession();

  const fetcher = React.useMemo(() => {
    return createGraphiQLFetcher({
      url: metadata?.GRAPHQL,
      headers: {
        ...(!!session?.orgId ? { "x-org-id": session.orgId } : {}),
        ...(!!session?.testMode ? { "x-test-mode": session.testMode } : {}),
        ...(!!session?.accessToken
          ? { authorization: `Bearer ${session.accessToken}` }
          : {}),
      },
    });
  }, [session.accessToken]);

  return (
    <div
      className="playground-wrapper"
      style={{ position: "absolute", top: 0, left: 0, bottom: 0, right: 0 }}
    >
      <EditorContextProvider>
        <ExecutionContextProvider fetcher={fetcher}>
          <ExplorerContextProvider>
            <HistoryContextProvider>
              <SchemaContextProvider fetcher={fetcher}>
                <StorageContextProvider>
                  <div className="graphiql-container" style={{ display: "flex", height: "100%" }}>
                    <div style={{ flex: 1, display: "flex", flexDirection: "column" }}>
                      <QueryEditor />
                      <VariableEditor />
                      <ResponseEditor />
                    </div>
                    <DocExplorer />
                  </div>
                </StorageContextProvider>
              </SchemaContextProvider>
            </HistoryContextProvider>
          </ExplorerContextProvider>
        </ExecutionContextProvider>
      </EditorContextProvider>
    </div>
  );
}
