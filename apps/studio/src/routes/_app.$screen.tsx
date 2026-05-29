import { Suspense } from "react";
import { createFileRoute, notFound } from "@tanstack/react-router";
import { ALL_ROUTES } from "~/lib/modes";
import { getScreen } from "~/screens/registry";

// Single dispatch route for every Studio screen. Validates the param against
// the known IA; unknown routes 404. As real screen files are added per phase,
// they can graduate out of the registry into their own route files.
export const Route = createFileRoute("/_app/$screen")({
  beforeLoad: ({ params }) => {
    if (!ALL_ROUTES.includes(params.screen)) throw notFound();
  },
  component: ScreenRoute,
});

function ScreenRoute() {
  const { screen } = Route.useParams();
  const Screen = getScreen(screen);
  return (
    <Suspense fallback={<div className="page" data-testid="screen-loading"><div className="state-row">Loading…</div></div>}>
      <Screen />
    </Suspense>
  );
}
