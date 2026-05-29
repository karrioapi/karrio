// registry.tsx — maps a route to its screen component.
// Phase 0 (foundation): Home is a light demo; every other route renders a
// Placeholder so the full IA is navigable. Later phases replace placeholders
// with real screens wired to Karrio GraphQL/REST via @karrio/hooks.
import type { ComponentType } from "react";
import { HomeScreen } from "~/screens/HomeScreen";
import { Placeholder } from "~/screens/Placeholder";
import { ShipmentsScreen } from "~/screens/ship/ShipmentsScreen";

const REGISTRY: Record<string, ComponentType> = {
  home: HomeScreen,
  shipments: ShipmentsScreen,
};

export function getScreen(route: string): ComponentType {
  return REGISTRY[route] ?? (() => <Placeholder route={route} />);
}
