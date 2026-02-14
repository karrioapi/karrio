/**
 * Karrio Elements – host-side mounting script (~3KB, no React).
 *
 * Usage:
 *   <script src="https://your-cdn/elements.js"></script>
 *   <script>
 *     // Rate Sheet Editor
 *     const editor = KarrioElements.mount('#editor', {
 *       host: 'https://api.karrio.io',
 *       token: 'key_...',
 *       rateSheetId: 'rsh_...',
 *       carrier: 'custom',
 *       connectionId: 'conn_...',
 *       iframeSrc: 'https://your-cdn/ratesheet.html',
 *     });
 *     editor.on('save', () => console.log('saved'));
 *     editor.on('close', () => editor.unmount());
 *
 *     // Developer Tools
 *     const devtools = KarrioElements.mountDevtools('#devtools', {
 *       host: 'https://api.karrio.io',
 *       token: 'key_...',
 *       iframeSrc: 'https://your-cdn/devtools.html',
 *     });
 *     devtools.on('close', () => devtools.unmount());
 *
 *     // Carrier Connections
 *     const connections = KarrioElements.mountConnections('#connections', {
 *       host: 'https://api.karrio.io',
 *       token: 'key_...',
 *       iframeSrc: 'https://your-cdn/connections.html',
 *     });
 *     connections.on('save', (d) => console.log('connection changed', d));
 *     connections.on('ratesheet', ({ rateSheetId, connectionId, carrier_name }) => {
 *       // Open rate sheet editor for this connection
 *       KarrioElements.mount('#editor', {
 *         host: 'https://api.karrio.io',
 *         token: 'key_...',
 *         rateSheetId,
 *         connectionId,
 *         carrier: carrier_name,
 *       });
 *     });
 *
 *     // Template Editor
 *     const tmpl = KarrioElements.mountTemplateEditor('#template', {
 *       host: 'https://api.karrio.io',
 *       token: 'key_...',
 *       templateId: 'tpl_...',
 *       iframeSrc: 'https://your-cdn/template-editor.html',
 *     });
 *     tmpl.on('save', () => console.log('saved'));
 *     tmpl.on('close', () => tmpl.unmount());
 *   </script>
 */

interface MountOptions {
  host: string;
  token: string;
  rateSheetId?: string;
  carrier?: string;
  connectionId?: string;
  /** Use admin GraphQL endpoint (/admin/graphql) instead of base (/graphql) */
  admin?: boolean;
  /** Full URL to the ratesheet.html iframe page */
  iframeSrc?: string;
}

interface DevtoolsMountOptions {
  host: string;
  token: string;
  /** Use admin GraphQL endpoint */
  admin?: boolean;
  /** Default tab to open: activity, api-keys, logs, events, apps, webhooks, playground, graphiql */
  defaultView?: string;
  /** Full URL to the devtools.html iframe page */
  iframeSrc?: string;
}

interface TemplateEditorMountOptions {
  host: string;
  token: string;
  /** Use admin GraphQL endpoint */
  admin?: boolean;
  /** ID of existing template to edit. Omit or 'new' for creation */
  templateId?: string;
  /** Full URL to the template-editor.html iframe page */
  iframeSrc?: string;
}

interface EditorHandle {
  on: (event: string, callback: (...args: any[]) => void) => EditorHandle;
  unmount: () => void;
  update: (opts: Partial<MountOptions>) => void;
}

interface DevtoolsHandle {
  on: (event: string, callback: (...args: any[]) => void) => DevtoolsHandle;
  unmount: () => void;
}

type Listener = (...args: any[]) => void;

function mount(selector: string | HTMLElement, options: MountOptions): EditorHandle {
  const container =
    typeof selector === "string"
      ? document.querySelector<HTMLElement>(selector)
      : selector;

  if (!container) {
    throw new Error(`[KarrioElements] Container not found: ${selector}`);
  }

  const listeners: Record<string, Listener[]> = {};
  let currentOptions = { ...options };

  // Build iframe src - default to same origin if not specified
  const iframeSrc =
    options.iframeSrc ||
    `${window.location.origin}/static/karrio/elements/ratesheet.html`;

  // Create iframe
  const iframe = document.createElement("iframe");
  iframe.src = iframeSrc;
  iframe.style.width = "100%";
  iframe.style.border = "none";
  iframe.style.minHeight = "600px";
  iframe.setAttribute("allowtransparency", "true");

  // Listen for messages from the iframe
  const handleMessage = (event: MessageEvent) => {
    const { data } = event;
    if (data?.source !== "karrio-embed") return;

    switch (data.type) {
      case "READY":
        // Iframe is ready – send config
        iframe.contentWindow?.postMessage(
          {
            source: "karrio-host",
            type: "INIT",
            host: currentOptions.host,
            token: currentOptions.token,
            rateSheetId: currentOptions.rateSheetId,
            carrier: currentOptions.carrier,
            connectionId: currentOptions.connectionId,
            admin: currentOptions.admin ?? false,
          },
          "*",
        );
        break;

      case "RESIZE":
        if (typeof data.height === "number") {
          iframe.style.height = `${data.height}px`;
        }
        break;

      case "EVENT":
        fire(data.event, data.payload);
        break;
    }
  };

  window.addEventListener("message", handleMessage);
  container.appendChild(iframe);

  function fire(event: string, ...args: any[]) {
    (listeners[event] || []).forEach((cb) => cb(...args));
  }

  const handle: EditorHandle = {
    on(event: string, callback: Listener) {
      if (!listeners[event]) listeners[event] = [];
      listeners[event].push(callback);
      return handle;
    },

    unmount() {
      window.removeEventListener("message", handleMessage);
      iframe.remove();
    },

    update(opts: Partial<MountOptions>) {
      currentOptions = { ...currentOptions, ...opts };
      // Re-send INIT with updated options
      iframe.contentWindow?.postMessage(
        {
          source: "karrio-host",
          type: "INIT",
          host: currentOptions.host,
          token: currentOptions.token,
          rateSheetId: currentOptions.rateSheetId,
          carrier: currentOptions.carrier,
          connectionId: currentOptions.connectionId,
          admin: currentOptions.admin ?? false,
        },
        "*",
      );
    },
  };

  return handle;
}

function mountDevtools(
  selector: string | HTMLElement,
  options: DevtoolsMountOptions,
): DevtoolsHandle {
  const container =
    typeof selector === "string"
      ? document.querySelector<HTMLElement>(selector)
      : selector;

  if (!container) {
    throw new Error(`[KarrioElements] Container not found: ${selector}`);
  }

  const listeners: Record<string, Listener[]> = {};

  const iframeSrc =
    options.iframeSrc ||
    `${window.location.origin}/static/karrio/elements/devtools.html`;

  const iframe = document.createElement("iframe");
  iframe.src = iframeSrc;
  iframe.style.width = "100%";
  iframe.style.height = "100%";
  iframe.style.border = "none";
  iframe.style.minHeight = "700px";
  iframe.setAttribute("allowtransparency", "true");

  const handleMessage = (event: MessageEvent) => {
    const { data } = event;
    if (data?.source !== "karrio-embed") return;

    switch (data.type) {
      case "READY":
        iframe.contentWindow?.postMessage(
          {
            source: "karrio-host",
            type: "INIT",
            host: options.host,
            token: options.token,
            admin: options.admin ?? false,
            defaultView: options.defaultView,
          },
          "*",
        );
        break;

      case "RESIZE":
        if (typeof data.height === "number") {
          iframe.style.height = `${Math.max(700, data.height)}px`;
        }
        break;

      case "EVENT":
        fire(data.event, data.payload);
        break;
    }
  };

  window.addEventListener("message", handleMessage);
  container.appendChild(iframe);

  function fire(event: string, ...args: any[]) {
    (listeners[event] || []).forEach((cb) => cb(...args));
  }

  const handle: DevtoolsHandle = {
    on(event: string, callback: Listener) {
      if (!listeners[event]) listeners[event] = [];
      listeners[event].push(callback);
      return handle;
    },

    unmount() {
      window.removeEventListener("message", handleMessage);
      iframe.remove();
    },
  };

  return handle;
}

function mountTemplateEditor(
  selector: string | HTMLElement,
  options: TemplateEditorMountOptions,
): EditorHandle {
  const container =
    typeof selector === "string"
      ? document.querySelector<HTMLElement>(selector)
      : selector;

  if (!container) {
    throw new Error(`[KarrioElements] Container not found: ${selector}`);
  }

  const listeners: Record<string, Listener[]> = {};
  let currentOptions = { ...options };

  const iframeSrc =
    options.iframeSrc ||
    `${window.location.origin}/static/karrio/elements/template-editor.html`;

  const iframe = document.createElement("iframe");
  iframe.src = iframeSrc;
  iframe.style.width = "100%";
  iframe.style.border = "none";
  iframe.style.minHeight = "600px";
  iframe.setAttribute("allowtransparency", "true");

  const handleMessage = (event: MessageEvent) => {
    const { data } = event;
    if (data?.source !== "karrio-embed") return;

    switch (data.type) {
      case "READY":
        iframe.contentWindow?.postMessage(
          {
            source: "karrio-host",
            type: "INIT",
            host: currentOptions.host,
            token: currentOptions.token,
            admin: currentOptions.admin ?? false,
            templateId: currentOptions.templateId,
          },
          "*",
        );
        break;

      case "RESIZE":
        if (typeof data.height === "number") {
          iframe.style.height = `${data.height}px`;
        }
        break;

      case "EVENT":
        fire(data.event, data.payload);
        break;
    }
  };

  window.addEventListener("message", handleMessage);
  container.appendChild(iframe);

  function fire(event: string, ...args: any[]) {
    (listeners[event] || []).forEach((cb) => cb(...args));
  }

  const handle: EditorHandle = {
    on(event: string, callback: Listener) {
      if (!listeners[event]) listeners[event] = [];
      listeners[event].push(callback);
      return handle;
    },

    unmount() {
      window.removeEventListener("message", handleMessage);
      iframe.remove();
    },

    update(opts: Partial<TemplateEditorMountOptions>) {
      currentOptions = { ...currentOptions, ...opts };
      iframe.contentWindow?.postMessage(
        {
          source: "karrio-host",
          type: "INIT",
          host: currentOptions.host,
          token: currentOptions.token,
          admin: currentOptions.admin ?? false,
          templateId: currentOptions.templateId,
        },
        "*",
      );
    },
  };

  return handle;
}

interface ConnectionsMountOptions {
  host: string;
  token: string;
  /** Use admin GraphQL endpoint */
  admin?: boolean;
  /** ID of existing connection to edit on mount */
  connectionId?: string;
  /** Pre-select carrier for new connection */
  carrier?: string;
  /** Full URL to the connections.html iframe page */
  iframeSrc?: string;
}

function mountConnections(
  selector: string | HTMLElement,
  options: ConnectionsMountOptions,
): EditorHandle {
  const container =
    typeof selector === "string"
      ? document.querySelector<HTMLElement>(selector)
      : selector;

  if (!container) {
    throw new Error(`[KarrioElements] Container not found: ${selector}`);
  }

  const listeners: Record<string, Listener[]> = {};
  let currentOptions = { ...options };

  const iframeSrc =
    options.iframeSrc ||
    `${window.location.origin}/static/karrio/elements/connections.html`;

  const iframe = document.createElement("iframe");
  iframe.src = iframeSrc;
  iframe.style.width = "100%";
  iframe.style.border = "none";
  iframe.style.minHeight = "400px";
  iframe.setAttribute("allowtransparency", "true");

  const handleMessage = (event: MessageEvent) => {
    const { data } = event;
    if (data?.source !== "karrio-embed") return;

    switch (data.type) {
      case "READY":
        iframe.contentWindow?.postMessage(
          {
            source: "karrio-host",
            type: "INIT",
            host: currentOptions.host,
            token: currentOptions.token,
            admin: currentOptions.admin ?? false,
            connectionId: currentOptions.connectionId,
            carrier: currentOptions.carrier,
          },
          "*",
        );
        break;

      case "RESIZE":
        if (typeof data.height === "number") {
          iframe.style.height = `${data.height}px`;
        }
        break;

      case "EVENT":
        fire(data.event, data.payload);
        break;
    }
  };

  window.addEventListener("message", handleMessage);
  container.appendChild(iframe);

  function fire(event: string, ...args: any[]) {
    (listeners[event] || []).forEach((cb) => cb(...args));
  }

  const handle: EditorHandle = {
    on(event: string, callback: Listener) {
      if (!listeners[event]) listeners[event] = [];
      listeners[event].push(callback);
      return handle;
    },

    unmount() {
      window.removeEventListener("message", handleMessage);
      iframe.remove();
    },

    update(opts: Partial<ConnectionsMountOptions>) {
      currentOptions = { ...currentOptions, ...opts };
      iframe.contentWindow?.postMessage(
        {
          source: "karrio-host",
          type: "INIT",
          host: currentOptions.host,
          token: currentOptions.token,
          admin: currentOptions.admin ?? false,
          connectionId: currentOptions.connectionId,
          carrier: currentOptions.carrier,
        },
        "*",
      );
    },
  };

  return handle;
}

// Expose on window as IIFE global
(window as any).KarrioElements = { mount, mountDevtools, mountTemplateEditor, mountConnections };

export { mount, mountDevtools, mountTemplateEditor, mountConnections };
export type { MountOptions, DevtoolsMountOptions, TemplateEditorMountOptions, ConnectionsMountOptions, EditorHandle, DevtoolsHandle };
