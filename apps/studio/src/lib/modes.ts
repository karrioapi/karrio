// modes.ts — Ship / Build / Govern information architecture.
// Mode is the core IA primitive: switching swaps the nav and jumps to the
// mode default route; mode is also auto-derived from the active route so
// deep links land in the right mode.
import { Icon, type IconName } from "~/components/ui/icons";

export type Mode = "ship" | "build" | "govern";

export type NavItem = {
  icon: IconName;
  label: string;
  route: string;
  badge?: string;
};

export type NavGroup = {
  label?: string;
  items: NavItem[];
};

export const MODE_LABELS: Record<Mode, { label: string; icon: IconName }> = {
  ship: { label: "Ship", icon: "Truck" },
  build: { label: "Build", icon: "Code" },
  govern: { label: "Govern", icon: "Shield" },
};

export const MODE_DEFAULTS: Record<Mode, string> = {
  ship: "home",
  build: "apps",
  govern: "admin",
};

export const NAV: Record<Mode, NavGroup[]> = {
  ship: [
    {
      items: [
        { icon: "Home", label: "Home", route: "home" },
        { icon: "Truck", label: "Shipments", route: "shipments" },
        { icon: "Pin", label: "Trackers", route: "trackers" },
        { icon: "Inbox", label: "Orders", route: "orders" },
        { icon: "Box", label: "Pickups", route: "pickups" },
      ],
    },
    {
      label: "Setup",
      items: [
        { icon: "Plug", label: "Connections", route: "connections" },
        { icon: "Activity", label: "Shipping rules", route: "rules" },
        { icon: "Pin", label: "Addresses", route: "addresses" },
        { icon: "Pkg", label: "Parcels", route: "parcels" },
        { icon: "Tag", label: "Products", route: "products" },
        { icon: "Doc", label: "Documents", route: "documents" },
      ],
    },
  ],
  build: [
    {
      items: [
        { icon: "Grid", label: "Apps", route: "apps" },
        { icon: "Plug", label: "Plugins", route: "plugins" },
        { icon: "Terminal", label: "MCP", route: "mcp" },
        { icon: "Code", label: "Editor", route: "editor" },
      ],
    },
    {
      label: "Developer",
      items: [
        { icon: "Webhook", label: "Webhooks", route: "webhooks" },
        { icon: "Key", label: "API keys", route: "apikeys" },
      ],
    },
  ],
  govern: [
    {
      items: [
        { icon: "Home", label: "Overview", route: "admin" },
        { icon: "Workspace", label: "Tenants", route: "tenants" },
        { icon: "User", label: "Team & roles", route: "team" },
        { icon: "Lock", label: "Security", route: "security" },
        { icon: "Doc", label: "Audit log", route: "audit" },
        { icon: "Settings", label: "Settings", route: "settings" },
      ],
    },
  ],
};

const BUILD_ROUTES = new Set([
  "apps",
  "plugins",
  "mcp",
  "editor",
  "webhooks",
  "apikeys",
]);
const GOVERN_ROUTES = new Set([
  "admin",
  "tenants",
  "team",
  "security",
  "audit",
  "settings",
]);

export function routeMode(route: string): Mode {
  if (BUILD_ROUTES.has(route)) return "build";
  if (GOVERN_ROUTES.has(route)) return "govern";
  return "ship";
}

// Flat list of every screen route — used by the splat route + tests.
export const ALL_ROUTES: string[] = Object.values(NAV)
  .flat()
  .flatMap((group) => group.items.map((item) => item.route));

// Re-export Icon so consumers importing from modes get a single source.
export { Icon };
