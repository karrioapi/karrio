import type { AppRouter } from "@karrio/console/trpc/router";
import { getBaseUrl } from "@karrio/console/utils";
import { httpBatchLink } from "@trpc/client";
import { createTRPCNext } from "@trpc/next";

export const trpc = createTRPCNext<AppRouter>({
  config(opts) {
    return {
      links: [
        httpBatchLink({
          /**
           * If you want to use SSR, you need to use the server's full URL
           * @see https://trpc.io/docs/v11/ssr
           **/
          url: `${getBaseUrl()}/api/trpc`,
          // You can pass any HTTP headers you wish here
          async headers() {
            return {
              // authorization: getAuthCookie(),
            };
          },
        }),
      ],
    };
  },
  /**
   * @see https://trpc.io/docs/v11/ssr
   **/
  ssr: false,
});
