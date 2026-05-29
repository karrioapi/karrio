// registry.tsx — route → screen component, code-split via React.lazy so each
// screen ships in its own chunk (smaller initial bundle; better Lighthouse).
import { lazy, type ComponentType } from "react";
import { HomeScreen } from "~/screens/HomeScreen";
import { Placeholder } from "~/screens/Placeholder";

const lz = (factory: () => Promise<{ [k: string]: ComponentType }>, name: string) =>
  lazy(() => factory().then((m) => ({ default: m[name] })));

const REGISTRY: Record<string, ComponentType> = {
  home: HomeScreen, // eager: default landing
  // Ship
  shipments: lz(() => import("~/screens/ship/ShipmentsScreen"), "ShipmentsScreen"),
  trackers: lz(() => import("~/screens/ship/TrackersScreen"), "TrackersScreen"),
  orders: lz(() => import("~/screens/ship/OrdersScreen"), "OrdersScreen"),
  pickups: lz(() => import("~/screens/ship/PickupsScreen"), "PickupsScreen"),
  connections: lz(() => import("~/screens/ship/ConnectionsScreen"), "ConnectionsScreen"),
  rules: lz(() => import("~/screens/ship/RulesScreen"), "RulesScreen"),
  addresses: lz(() => import("~/screens/ship/AddressesScreen"), "AddressesScreen"),
  parcels: lz(() => import("~/screens/ship/ParcelsScreen"), "ParcelsScreen"),
  products: lz(() => import("~/screens/ship/ProductsScreen"), "ProductsScreen"),
  documents: lz(() => import("~/screens/ship/DocumentsScreen"), "DocumentsScreen"),
  // Build
  apps: lz(() => import("~/screens/build/AppsScreen"), "AppsScreen"),
  plugins: lz(() => import("~/screens/build/PluginsScreen"), "PluginsScreen"),
  mcp: lz(() => import("~/screens/build/McpScreen"), "McpScreen"),
  webhooks: lz(() => import("~/screens/build/WebhooksScreen"), "WebhooksScreen"),
  apikeys: lz(() => import("~/screens/build/ApiKeysScreen"), "ApiKeysScreen"),
  editor: lz(() => import("~/screens/build/EditorScreen"), "EditorScreen"),
  // Govern
  admin: lz(() => import("~/screens/govern/AdminScreen"), "AdminScreen"),
  tenants: lz(() => import("~/screens/govern/TenantsScreen"), "TenantsScreen"),
  team: lz(() => import("~/screens/govern/TeamScreen"), "TeamScreen"),
  security: lz(() => import("~/screens/govern/SecurityScreen"), "SecurityScreen"),
  audit: lz(() => import("~/screens/govern/AuditScreen"), "AuditScreen"),
  settings: lz(() => import("~/screens/govern/SettingsScreen"), "SettingsScreen"),
};

export function getScreen(route: string): ComponentType {
  return REGISTRY[route] ?? (() => <Placeholder route={route} />);
}
