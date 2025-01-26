import { KarrioPlatformClient } from "@karrio/console/types/api";
import { AxiosRequestHeaders } from "axios";
import { TRPCError } from "@trpc/server";

const client = KarrioPlatformClient({
  basePath: process.env.KARRIO_PLATFORM_API_URL!,
  headers: {
    Authorization: `Token ${process.env.KARRIO_PLATFORM_API_KEY}`,
  } as AxiosRequestHeaders,
});

// Helper function to handle GraphQL requests
export async function karrio<T>(
  query: string,
  variables: any,
  errorMessage: string,
): Promise<T> {
  try {
    const response = await client.request<T>(query, { variables });
    return response;
  } catch (error: any) {
    console.error(error.data);
    throw new TRPCError({
      code: "INTERNAL_SERVER_ERROR",
      message: error.data?.errors?.[0]?.message || errorMessage,
    });
  }
}
