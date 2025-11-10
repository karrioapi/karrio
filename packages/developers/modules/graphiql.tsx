"use client";
import React from "react";
import { useAPIMetadata } from "@karrio/hooks/api-metadata";
import { createGraphiQLFetcher } from "@graphiql/toolkit";
import { useSyncedSession } from "@karrio/hooks/session";
import { GraphiQL } from "graphiql";
import "graphiql/graphiql.min.css";

export function GraphiQLModule() {
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
        ...(session?.testMode ? { "x-test-mode": session.testMode.toString() } : {}),
        ...(session?.accessToken
          ? { authorization: `Bearer ${session.accessToken}` }
          : {}),
      },
    });
  }, [metadata?.GRAPHQL, session?.accessToken, session?.orgId, session?.testMode]);

  if (!fetcher) {
    return (
      <div className="flex items-center justify-center h-full">
        <div className="text-muted-foreground">Loading GraphQL Explorer...</div>
      </div>
    );
  }

  // Create portal container and move modals to it
  React.useEffect(() => {
    const portalContainer = document.createElement('div');
    portalContainer.id = 'graphiql-portal';
    portalContainer.style.position = 'fixed';
    portalContainer.style.top = '0';
    portalContainer.style.left = '0';
    portalContainer.style.width = '100%';
    portalContainer.style.height = '100%';
    portalContainer.style.pointerEvents = 'none';
    portalContainer.style.zIndex = '10000';
    document.body.appendChild(portalContainer);

    // Watch for GraphiQL modals and move them to portal
    const observer = new MutationObserver((mutations) => {
      mutations.forEach((mutation) => {
        mutation.addedNodes.forEach((node) => {
          if (node.nodeType === Node.ELEMENT_NODE) {
            const element = node as Element;
            // Check if it's a GraphiQL modal overlay
            if (element.classList.contains('graphiql-dialog-overlay') ||
              element.querySelector('.graphiql-dialog-overlay')) {
              portalContainer.appendChild(element);
              portalContainer.style.pointerEvents = 'auto';
            }
          }
        });
      });
    });

    // Start observing the document body for modal additions
    observer.observe(document.body, {
      childList: true,
      subtree: true
    });

    return () => {
      observer.disconnect();
      const existingContainer = document.getElementById('graphiql-portal');
      if (existingContainer) {
        document.body.removeChild(existingContainer);
      }
    };
  }, []);

  // Layout sizing handled by the drawer; no additional measurements needed

  return (
    <div className="h-full w-full overflow-hidden">
      <div className="h-full relative">
        <style jsx global>{`
          .graphiql-container { height: 100% !important; }

          /* Scoped dark theme overrides */
          .devtools-theme.dark .graphiql-container { background: hsl(var(--background)) !important; color: hsl(var(--foreground)) !important; }
          .devtools-theme.dark .graphiql-main,
          .devtools-theme.dark .graphiql-editors,
          .devtools-theme.dark .graphiql-editor,
          .devtools-theme.dark .graphiql-sidebar,
          .devtools-theme.dark .graphiql-doc-explorer { background: hsl(var(--card)) !important; }
          .devtools-theme.dark .graphiql-toolbar button,
          .devtools-theme.dark .graphiql-toolbar select,
          .devtools-theme.dark .graphiql-toolbar input { color: hsl(var(--foreground)) !important; border-color: hsl(var(--border)) !important; background: hsl(var(--input)) !important; }
          .devtools-theme.dark .graphiql-dialog { background: hsl(var(--popover)) !important; color: hsl(var(--popover-foreground)) !important; }
          
          /* Toolbar layout and sizing */
          .devtools-theme.dark .graphiql-toolbar { display: flex !important; flex-wrap: nowrap !important; gap: 8px !important; align-items: center !important; }
          .devtools-theme.dark .graphiql-execute { display: flex !important; align-items: center !important; }
          .devtools-theme.dark .graphiql-toolbar button,
          .devtools-theme.dark .graphiql-execute button { height: 40px !important; padding: 0 12px !important; border-radius: 8px !important; font-size: 15px !important; }
          .devtools-theme.dark .graphiql-toolbar button svg { width: 24px !important; height: 24px !important; }
          .devtools-theme.dark .graphiql-execute button { display: inline-flex !important; align-items: center !important; justify-content: center !important; }
          .devtools-theme.dark .graphiql-execute button svg { width: 16px !important; height: 16px !important; }
          
          /* Force GraphiQL modals to use the portal container */
          .graphiql-dialog-overlay {
            position: fixed !important;
            top: 0 !important;
            left: 0 !important;
            right: 0 !important;
            bottom: 0 !important;
            z-index: 10000 !important;
            background-color: rgba(0, 0, 0, 0.5) !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            pointer-events: auto !important;
          }
          
          /* Ensure all GraphiQL UI elements appear above drawer with high z-index */
          .graphiql-dialog,
          .graphiql-tooltip,
          .graphiql-menu,
          .graphiql-dialog-section,
          .CodeMirror-hints,
          .CodeMirror-hint-active {
            z-index: 10000 !important;
            pointer-events: auto !important;
          }
          
          /* Force modals to be appended to portal container */
          .graphiql-dialog-overlay {
            /* This will be moved to the portal via JavaScript */
          }
          
          /* Ensure proper text rendering in GraphiQL editors */
          .graphiql-editor,
          .graphiql-editor .CodeMirror,
          .graphiql-editor .CodeMirror-scroll { height: 100% !important; }
          
          /* Fix text visibility issues */
          .graphiql-editor .CodeMirror,
          .graphiql-editor .CodeMirror-code,
          .graphiql-editor .CodeMirror-lines,
          .graphiql-editor .CodeMirror-line { background: transparent !important; }
          
          .devtools-theme.dark .graphiql-editor .CodeMirror-cursor { border-left: 1px solid hsl(var(--foreground)) !important; opacity: 0.6; }
          
          /* Use editor theme defaults; avoid hard-coded syntax colors */
          .graphiql-editor .cm-keyword,
          .graphiql-editor .cm-string,
          .graphiql-editor .cm-number,
          .graphiql-editor .cm-comment,
          .graphiql-editor .cm-property,
          .graphiql-editor .cm-punctuation,
          .graphiql-editor .cm-bracket { color: inherit !important; }
          
          /* Ensure editor containers have proper dimensions */
          .graphiql-editor-tools,
          .graphiql-query-editor,
          .graphiql-variable-editor,
          .graphiql-result { flex: 1 !important; display: flex !important; flex-direction: column !important; min-height: 0 !important; }
          .graphiql-main, .graphiql-editors { display:flex !important; flex:1 1 auto !important; min-height:0 !important; }
          .graphiql-editor .CodeMirror, .graphiql-editor .CodeMirror-scroll { height:100% !important; }
          
          
          .graphiql-dialog { border-radius: 6px !important; box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2) !important; max-width: 90vw !important; max-height: 90vh !important; overflow: auto !important; }
        `}</style>
        <div className="h-full w-full overflow-x-auto lg:overflow-x-hidden" style={{ WebkitOverflowScrolling: 'touch', overscrollBehaviorX: 'contain', touchAction: 'pan-x' as any }}>
          <div className="h-full w-[1200px] lg:w-full">
            <GraphiQL fetcher={fetcher as any} />
          </div>
        </div>
      </div>
    </div>
  );
}