import type { AppRouter } from "@karrio/console/trpc/router";
import { createTRPCReact } from "@trpc/react-query";

export const trpc = createTRPCReact<AppRouter>();
