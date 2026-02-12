import React, { useEffect, useState } from "react";
import { createRoot } from "react-dom/client";
import { KarrioEmbedProvider } from "../providers/karrio-embed-provider";
import { APIMetadataEmbedProvider } from "../providers/api-metadata-embed-provider";
import {
  DeveloperToolsProvider,
  useDeveloperTools,
} from "@karrio/developers/context/developer-tools-context";
import { DeveloperToolsDrawer } from "@karrio/developers/components/developer-tools-drawer";
import { Toaster } from "@karrio/ui/components/ui/toaster";
import "../styles/globals.css";

import type { DeveloperView } from "@karrio/developers/context/developer-tools-context";

interface InitConfig {
  host: string;
  token: string;
  admin?: boolean;
  defaultView?: DeveloperView;
}

/** Automatically opens the devtools drawer on mount */
function AutoOpen({ defaultView }: { defaultView?: DeveloperView }) {
  const { openDeveloperTools, isOpen } = useDeveloperTools();

  useEffect(() => {
    if (!isOpen) {
      openDeveloperTools(defaultView || "activity");
    }
  }, []); // eslint-disable-line react-hooks/exhaustive-deps

  return null;
}

/** Sends a close event to the host only after the drawer has been opened once */
function CloseWatcher() {
  const { isOpen } = useDeveloperTools();
  const hasOpened = React.useRef(false);

  useEffect(() => {
    if (isOpen) {
      hasOpened.current = true;
    } else if (hasOpened.current) {
      // Only fire close after the drawer was open at least once
      window.parent.postMessage(
        { source: "karrio-embed", type: "EVENT", event: "close" },
        "*",
      );
    }
  }, [isOpen]);

  return null;
}

function DevtoolsApp({ config }: { config: InitConfig }) {
  return (
    <KarrioEmbedProvider host={config.host} token={config.token} admin={config.admin}>
      <APIMetadataEmbedProvider>
        <DeveloperToolsProvider>
          <AutoOpen defaultView={config.defaultView} />
          <CloseWatcher />
          <DeveloperToolsDrawer />
          <Toaster />
        </DeveloperToolsProvider>
      </APIMetadataEmbedProvider>
    </KarrioEmbedProvider>
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
          admin: data.admin ?? false,
          defaultView: data.defaultView,
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
      <div className="flex items-center justify-center h-screen dark bg-background">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-gray-400" />
      </div>
    );
  }

  return <DevtoolsApp config={config} />;
}

const root = createRoot(document.getElementById("root")!);
root.render(<App />);
