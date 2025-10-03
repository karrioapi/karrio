import { fetchRequestHandler } from "@trpc/server/adapters/fetch";
import { createContext } from "@karrio/console/trpc/context";
import { appRouter } from "@karrio/console/trpc/router";

export const handler = (request: Request) => {
  return fetchRequestHandler({
    endpoint: "/api/trpc",
    router: appRouter,
    req: request,
    createContext,
  });
};
