import React, { useEffect, useState, useMemo } from "react";
import { createRoot } from "react-dom/client";
import { KarrioEmbedProvider } from "../providers/karrio-embed-provider";
import { APIMetadataEmbedProvider } from "../providers/api-metadata-embed-provider";
import { useRateSheet, useRateSheetMutation } from "../hooks/embed-rate-sheet";
import { useEmbedMarkups, useEmbedMarkupMutation } from "../hooks/embed-markups";
import RateSheetEditor from "@karrio/ui/components/rate-sheet-editor";
import { Toaster } from "@karrio/ui/components/ui/toaster";
import "../styles/globals.css";

interface InitConfig {
  host: string;
  token: string;
  rateSheetId?: string;
  carrier?: string;
  connectionId?: string;
  admin?: boolean;
}

function RateSheetApp({ config }: { config: InitConfig }) {
  const handleClose = () => {
    window.parent.postMessage(
      { source: "karrio-embed", type: "EVENT", event: "close" },
      "*",
    );
  };

  return (
    <KarrioEmbedProvider host={config.host} token={config.token} admin={config.admin}>
      <APIMetadataEmbedProvider>
        <RateSheetEditorWithMarkups config={config} onClose={handleClose} />
        <Toaster />
      </APIMetadataEmbedProvider>
    </KarrioEmbedProvider>
  );
}

function RateSheetEditorWithMarkups({
  config,
  onClose,
}: {
  config: InitConfig;
  onClose: () => void;
}) {
  const isAdmin = !!config.admin;
  const { markups: markupsData } = useEmbedMarkups(isAdmin);
  const markupMutations = useEmbedMarkupMutation();

  return (
    <RateSheetEditor
      rateSheetId={config.rateSheetId || "new"}
      onClose={onClose}
      preloadCarrier={config.carrier}
      linkConnectionId={config.connectionId}
      isAdmin={isAdmin}
      useRateSheet={useRateSheet}
      useRateSheetMutation={useRateSheetMutation}
      markups={isAdmin ? markupsData : undefined}
      markupMutations={isAdmin ? markupMutations : undefined}
    />
  );
}

function App() {
  const [config, setConfig] = useState<InitConfig | null>(null);

  useEffect(() => {
    const handleMessage = (event: MessageEvent) => {
      const { data } = event;
      if (data?.source !== "karrio-host") return;

      if (data.type === "INIT") {
        setConfig({
          host: data.host,
          token: data.token,
          rateSheetId: data.rateSheetId,
          carrier: data.carrier,
          connectionId: data.connectionId,
          admin: data.admin ?? false,
        });
      }
    };

    window.addEventListener("message", handleMessage);

    // Signal to host that iframe is ready to receive INIT
    window.parent.postMessage(
      { source: "karrio-embed", type: "READY" },
      "*",
    );

    return () => window.removeEventListener("message", handleMessage);
  }, []);

  useEffect(() => {
    // Auto-resize: notify host of iframe content height changes
    const observer = new ResizeObserver((entries) => {
      for (const entry of entries) {
        window.parent.postMessage(
          {
            source: "karrio-embed",
            type: "RESIZE",
            height: entry.contentRect.height,
          },
          "*",
        );
      }
    });

    observer.observe(document.body);
    return () => observer.disconnect();
  }, []);

  if (!config) {
    return (
      <div className="flex items-center justify-center h-screen">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-gray-400" />
      </div>
    );
  }

  return <RateSheetApp config={config} />;
}

const root = createRoot(document.getElementById("root")!);
root.render(<App />);
