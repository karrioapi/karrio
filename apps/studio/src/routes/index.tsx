import { createFileRoute, redirect } from "@tanstack/react-router";

// Root → Ship mode default route.
export const Route = createFileRoute("/")({
  beforeLoad: () => {
    throw redirect({ to: "/$screen", params: { screen: "home" } });
  },
});
