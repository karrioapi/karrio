// registry.tsx — maps a route to its screen component.
// Phase 0 (foundation): Home is a light demo; every other route renders a
// Placeholder so the full IA is navigable. Later phases replace placeholders
// with real screens wired to Karrio GraphQL/REST via @karrio/hooks.
import type { ComponentType } from "react";
import { HomeScreen } from "~/screens/HomeScreen";
import { Placeholder } from "~/screens/Placeholder";
import { ShipmentsScreen } from "~/screens/ship/ShipmentsScreen";
import { TrackersScreen } from "~/screens/ship/TrackersScreen";
import { OrdersScreen } from "~/screens/ship/OrdersScreen";
import { PickupsScreen } from "~/screens/ship/PickupsScreen";
import { ConnectionsScreen } from "~/screens/ship/ConnectionsScreen";
import { RulesScreen } from "~/screens/ship/RulesScreen";
import { AddressesScreen } from "~/screens/ship/AddressesScreen";
import { ParcelsScreen } from "~/screens/ship/ParcelsScreen";
import { ProductsScreen } from "~/screens/ship/ProductsScreen";
import { DocumentsScreen } from "~/screens/ship/DocumentsScreen";
import { AppsScreen } from "~/screens/build/AppsScreen";
import { PluginsScreen } from "~/screens/build/PluginsScreen";
import { McpScreen } from "~/screens/build/McpScreen";
import { WebhooksScreen } from "~/screens/build/WebhooksScreen";
import { ApiKeysScreen } from "~/screens/build/ApiKeysScreen";
import { EditorScreen } from "~/screens/build/EditorScreen";
import { AdminScreen } from "~/screens/govern/AdminScreen";
import { TenantsScreen } from "~/screens/govern/TenantsScreen";
import { TeamScreen } from "~/screens/govern/TeamScreen";
import { SecurityScreen } from "~/screens/govern/SecurityScreen";
import { AuditScreen } from "~/screens/govern/AuditScreen";
import { SettingsScreen } from "~/screens/govern/SettingsScreen";

const REGISTRY: Record<string, ComponentType> = {
  home: HomeScreen,
  shipments: ShipmentsScreen,
  trackers: TrackersScreen,
  orders: OrdersScreen,
  pickups: PickupsScreen,
  connections: ConnectionsScreen,
  rules: RulesScreen,
  addresses: AddressesScreen,
  parcels: ParcelsScreen,
  products: ProductsScreen,
  documents: DocumentsScreen,
  apps: AppsScreen,
  plugins: PluginsScreen,
  mcp: McpScreen,
  webhooks: WebhooksScreen,
  apikeys: ApiKeysScreen,
  editor: EditorScreen,
  admin: AdminScreen,
  tenants: TenantsScreen,
  team: TeamScreen,
  security: SecurityScreen,
  audit: AuditScreen,
  settings: SettingsScreen,
};

export function getScreen(route: string): ComponentType {
  return REGISTRY[route] ?? (() => <Placeholder route={route} />);
}
