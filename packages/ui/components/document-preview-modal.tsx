"use client";

import React from "react";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
} from "./ui/dialog";
import { Button } from "./ui/button";
import { Loader2, Download, ExternalLink } from "lucide-react";

export type DocumentPreviewState = {
  isOpen: boolean;
  url: string | null;
  title: string;
  isLoading: boolean;
};

interface DocumentPreviewDialogProps {
  state: DocumentPreviewState;
  onClose: () => void;
}

export function DocumentPreviewDialog({
  state,
  onClose,
}: DocumentPreviewDialogProps): JSX.Element {
  const [iframeLoading, setIframeLoading] = React.useState(true);

  const handleOpenExternal = () => {
    state.url && window.open(state.url, "_blank");
  };

  const handleDownload = () => {
    if (!state.url) return;
    const link = document.createElement("a");
    link.href = state.url;
    link.download = "";
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  const handleIframeLoad = () => {
    setIframeLoading(false);
  };

  React.useEffect(() => {
    if (state.isOpen) {
      setIframeLoading(true);
    }
  }, [state.isOpen, state.url]);

  const isLoading = state.isLoading || iframeLoading;

  return (
    <Dialog open={state.isOpen} onOpenChange={(open) => !open && onClose()}>
      <DialogContent className="max-w-[95vw] w-[95vw] h-[90vh] max-h-[90vh]">
        <DialogHeader className="flex flex-row items-center justify-between pr-10">
          <DialogTitle className="flex items-center gap-2">
            {isLoading && <Loader2 className="h-4 w-4 animate-spin" />}
            {state.title}
          </DialogTitle>
          <div className="flex items-center gap-2">
            <Button
              variant="outline"
              size="sm"
              onClick={handleDownload}
              disabled={!state.url || isLoading}
            >
              <Download className="h-4 w-4 mr-1" />
              Download
            </Button>
            <Button
              variant="outline"
              size="sm"
              onClick={handleOpenExternal}
              disabled={!state.url || isLoading}
            >
              <ExternalLink className="h-4 w-4 mr-1" />
              Open in New Tab
            </Button>
          </div>
        </DialogHeader>

        <div className="flex-1 w-full h-full min-h-0 relative bg-muted/30 rounded-md">
          {isLoading && (
            <div className="absolute inset-0 flex flex-col items-center justify-center bg-background/80 z-10 gap-3">
              <Loader2 className="h-10 w-10 animate-spin text-muted-foreground" />
              <p className="text-sm text-muted-foreground">Loading document...</p>
            </div>
          )}
          {state.url && (
            <iframe
              src={state.url}
              className="w-full h-full border-0 rounded-md"
              title={state.title}
              onLoad={handleIframeLoad}
            />
          )}
        </div>
      </DialogContent>
    </Dialog>
  );
}

// Hook for managing document preview state
export function useDocumentPreviewState() {
  const [state, setState] = React.useState<DocumentPreviewState>({
    isOpen: false,
    url: null,
    title: "Document Preview",
    isLoading: false,
  });

  const openDocument = React.useCallback((url: string, title = "Document Preview") => {
    setState({ isOpen: true, url, title, isLoading: false });
  }, []);

  const closeDocument = React.useCallback(() => {
    setState({ isOpen: false, url: null, title: "Document Preview", isLoading: false });
  }, []);

  const setLoading = React.useCallback((isLoading: boolean) => {
    setState((prev) => ({
      ...prev,
      isLoading,
      isOpen: isLoading ? true : prev.isOpen,
    }));
  }, []);

  return {
    state,
    openDocument,
    closeDocument,
    setLoading,
  };
}
