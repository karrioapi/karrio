import type React from "react";

// App Manifest inspired by Stripe's app manifest
export interface AppManifest {
  // Basic app information
  id: string;
  name: string;
  slug: string;
  version: string;
  description: string;
  developer: {
    name: string;
    email: string;
    website?: string;
  };

  // App configuration
  category: AppCategory;
  type: AppType;
  logo: string; // Path to logo asset
  screenshots?: string[]; // Optional screenshots

  // Feature flags
  features: AppFeature[];

  // App capabilities
  oauth?: {
    required: boolean;
    scopes: string[];
  };

  // App embedding configuration
  ui?: {
    // Where this app can be embedded
    viewports: AppViewport[];
    // App settings component
    settings?: boolean;
  };

  // Installation requirements
  requirements?: {
    // Minimum Karrio version
    karrio_version?: string;
    // Required modules
    modules?: string[];
  };

  // Webhooks this app listens to
  webhooks?: {
    events: WebhookEvent[];
    endpoint?: string;
  };

  // Additional metadata
  metadata?: Record<string, any>;

  // Metafields schema for app configuration
  metafields?: MetafieldSchema[];
}

export type AppCategory =
  | "shipping"
  | "fulfillment"
  | "analytics"
  | "crm"
  | "ecommerce"
  | "automation"
  | "utility"
  | "integration";

export type AppType =
  | "builtin"     // Built-in Karrio apps
  | "marketplace" // Public marketplace apps
  | "private"     // Private/custom apps
  | "embedded";   // Embedded third-party apps

export type AppFeature =
  | "shipments"
  | "orders"
  | "tracking"
  | "customs"
  | "manifests"
  | "webhooks"
  | "analytics"
  | "automation";

export type AppViewport =
  | "dashboard"
  | "shipments"
  | "orders"
  | "tracking"
  | "settings"
  | "everywhere";

export type WebhookEvent =
  | "shipment.created"
  | "shipment.updated"
  | "order.created"
  | "order.updated"
  | "tracking.updated";

// Metafield schema for app configuration
export interface MetafieldSchema {
  key: string;
  label: string;
  type: MetafieldType;
  description?: string;
  is_required: boolean;
  default_value?: any;
  placeholder?: string;
  options?: { value: string; label: string }[];
  validation?: {
    min?: number;
    max?: number;
    step?: number;
    format?: string;
    enum?: string[];
  };
  sensitive?: boolean; // For passwords/API keys
}

export type MetafieldType =
  | "string"
  | "number"
  | "boolean"
  | "url"
  | "email"
  | "password"
  | "text"
  | "select"
  | "multiselect"
  | "date"
  | "datetime";

// App component types
export interface AppComponentProps {
  app: AppInstance;
  context: AppContext;
  onAction?: (action: AppAction) => void;
}

export interface AppInstance {
  id: string;
  manifest: AppManifest;
  installation?: AppInstallation;
  config?: Record<string, any>;
  isInstalled: boolean;
  isEnabled: boolean;
}

export interface AppInstallation {
  id: string;
  app_id: string;
  access_scopes: string[];
  config: Record<string, any>;
  metadata: Record<string, any>;
  installed_at: string;
  updated_at: string;
  metafields?: {
    id: string;
    key: string;
    value: string | null;
    is_required: boolean;
    type: string;
  }[];
}

export interface AppContext {
  // Current workspace/organization
  workspace: {
    id: string;
    name: string;
  };

  // Current user
  user?: {
    id: string;
    email: string;
    name: string;
  };

  // Current page context
  page?: {
    route: string;
    params: Record<string, string>;
  };

  // Data context (if applicable)
  data?: {
    shipment?: any;
    order?: any;
    tracking?: any;
  };
}

export interface AppAction {
  type: string;
  payload?: any;
  meta?: Record<string, any>;
}

// App settings component type
export interface AppSettingsComponentProps {
  app: AppInstance;
  config: Record<string, any>;
  onConfigChange: (config: Record<string, any>) => void;
  onSave: () => void;
  onCancel: () => void;
}

// App container types
export interface AppContainerProps {
  appId: string;
  viewport?: AppViewport;
  context?: Partial<AppContext>;
  className?: string;
}

// App store types
export interface AppStoreConfig {
  // Registry of available apps
  apps: Record<string, () => Promise<AppModule>>;

  // App loading configuration
  loading?: {
    timeout?: number;
    retries?: number;
  };
}

export interface AppModule {
  default: AppManifest;
  Component?: React.ComponentType<AppComponentProps>;
  SettingsComponent?: React.ComponentType<AppSettingsComponentProps>;
}

// Installation flow types
export interface AppInstallationFlow {
  app: AppManifest;
  step: InstallationStep;
  data: Record<string, any>;
  errors?: Record<string, string>;
}

export type InstallationStep =
  | "permissions"
  | "configuration"
  | "oauth"
  | "verification"
  | "complete";

// Error types
export interface AppError {
  code: string;
  message: string;
  details?: Record<string, any>;
}

export interface AppLoadError extends AppError {
  app_id: string;
}

// Utility types
export type AppStatus =
  | "loading"
  | "ready"
  | "error"
  | "installing"
  | "uninstalling";

export interface AppMetrics {
  installations: number;
  active_users: number;
  api_calls: number;
  errors: number;
  last_used?: string;
}
