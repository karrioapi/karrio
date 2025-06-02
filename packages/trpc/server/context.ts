import { type inferAsyncReturnType } from "@trpc/server";
import { getCurrentDomain, loadMetadata } from "@karrio/core/context/main";
import { KARRIO_API } from "@karrio/lib/constants";
import { auth } from "@karrio/core/context/auth";
import { KarrioClient } from "@karrio/types";
import type { Session } from "next-auth";
import { url$ } from "@karrio/lib";

export const createContext = async () => {
  const session = (await auth()) as Session | any | null;
  const domain = await getCurrentDomain();
  const { metadata } = await loadMetadata(domain!);
  const karrio = new KarrioClient({
    basePath: url$`${(metadata?.HOST as string) || KARRIO_API}`,
    headers: {
      ...(session?.orgId ? { "x-org-id": session.orgId } : {}),
      ...(session?.testMode ? { "x-test-mode": session.testMode } : {}),
      ...(session?.accessToken
        ? { Authorization: `Bearer ${session.accessToken}` }
        : {}),
    } as any,
  })

  return {
    karrio,
    session,
    user: session?.user,
  };
};

export type Context = inferAsyncReturnType<typeof createContext>;
