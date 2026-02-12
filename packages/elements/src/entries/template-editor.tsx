import React, { useEffect, useState } from "react";
import { createRoot } from "react-dom/client";
import { KarrioEmbedProvider } from "../providers/karrio-embed-provider";
import { APIMetadataEmbedProvider } from "../providers/api-metadata-embed-provider";
import { TemplateEditor } from "@karrio/ui/components/template-editor";
import { Toaster } from "@karrio/ui/components/ui/toaster";
import "../styles/globals.css";

interface InitConfig {
  host: string;
  token: string;
  admin?: boolean;
  templateId?: string;
}

function TemplateEditorApp({ config }: { config: InitConfig }) {
  const templateId = config.templateId || "new";

  const handleClose = () => {
    window.parent.postMessage(
      { source: "karrio-embed", type: "EVENT", event: "close" },
      "*",
    );
  };

  const handleSave = () => {
    window.parent.postMessage(
      { source: "karrio-embed", type: "EVENT", event: "save" },
      "*",
    );
  };

  return (
    <KarrioEmbedProvider host={config.host} token={config.token} admin={config.admin}>
      <APIMetadataEmbedProvider>
        <TemplateEditor
          templateId={templateId}
          onClose={handleClose}
          onSave={handleSave}
        />
        <Toaster />
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
          templateId: data.templateId,
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
      <div className="flex items-center justify-center h-screen bg-background">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-gray-400" />
      </div>
    );
  }

  return <TemplateEditorApp config={config} />;
}

const root = createRoot(document.getElementById("root")!);
root.render(<App />);
