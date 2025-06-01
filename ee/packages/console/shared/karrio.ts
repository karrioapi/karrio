import { KarrioPlatformClient } from "@karrio/console/types/api";
import { AxiosRequestHeaders } from "axios";
import { TRPCError } from "@trpc/server";
import "./environment"; // Import to trigger environment validation

// Log configuration details (without exposing sensitive data)
const API_URL = process.env.KARRIO_PLATFORM_API_URL;
const API_KEY_EXISTS = !!process.env.KARRIO_PLATFORM_API_KEY;
const API_KEY_PREFIX = process.env.KARRIO_PLATFORM_API_KEY?.substring(0, 8) + "...";

console.log(`[Karrio Client] API URL: ${API_URL}`);
console.log(`[Karrio Client] API Key configured: ${API_KEY_EXISTS}`);
console.log(`[Karrio Client] API Key prefix: ${API_KEY_PREFIX}`);

const client = KarrioPlatformClient({
  basePath: process.env.KARRIO_PLATFORM_API_URL!,
  headers: {
    Authorization: `Token ${process.env.KARRIO_PLATFORM_API_KEY}`,
  } as AxiosRequestHeaders,
});

// Health check function to verify connectivity
export async function healthCheck(): Promise<boolean> {
  try {
    console.log('[Karrio Health] Starting health check...');

    // Simple query to test connectivity and authentication
    const response = await client.request(`
      query {
        tenants(filter: { limit: 1 }) {
          edges {
            node {
              id
            }
          }
        }
      }
    `, {});

    console.log('[Karrio Health] Health check passed', {
      hasResponse: !!response,
      timestamp: new Date().toISOString(),
    });

    return true;
  } catch (error: any) {
    console.error('[Karrio Health] Health check failed', {
      errorMessage: error.message,
      errorStatus: error.response?.status,
      errorData: error.response?.data,
      apiUrl: API_URL,
      apiKeyConfigured: API_KEY_EXISTS,
      timestamp: new Date().toISOString(),
    });

    return false;
  }
}

// Run health check on module load (non-blocking)
healthCheck().catch(error => {
  console.warn('[Karrio Health] Initial health check failed, but continuing...', error.message);
});

// Helper function to handle GraphQL requests
export async function karrio<T>(
  query: string,
  variables: any,
  errorMessage: string,
  context?: { operation?: string; userId?: string; orgId?: string },
): Promise<T> {
  const startTime = Date.now();
  const operationName = query.match(/(?:mutation|query)\s+(\w+)/)?.[1] || 'unknown';

  console.log(`[Karrio API] Starting ${operationName}`, {
    operation: context?.operation || operationName,
    userId: context?.userId,
    orgId: context?.orgId,
    variablesKeys: Object.keys(variables || {}),
    timestamp: new Date().toISOString(),
  });

  try {
    const response = await client.request<T>(query, { variables });
    const duration = Date.now() - startTime;

    console.log(`[Karrio API] Success ${operationName}`, {
      operation: context?.operation || operationName,
      duration: `${duration}ms`,
      responseKeys: response ? Object.keys(response) : [],
      timestamp: new Date().toISOString(),
    });

    return response;
  } catch (error: any) {
    const duration = Date.now() - startTime;

    console.log(JSON.stringify(error?.data || {}, null, 2), ">>>>>>>");

    // Enhanced error logging
    console.error(`[Karrio API] Error ${operationName}`, {
      operation: context?.operation || operationName,
      duration: `${duration}ms`,
      errorMessage: error.message,
      errorData: error.data,
      errorResponse: error.response?.data,
      errorStatus: error.response?.status,
      errorHeaders: error.response?.headers,
      requestUrl: error.config?.url,
      requestMethod: error.config?.method,
      requestHeaders: error.config?.headers ? {
        ...error.config.headers,
        Authorization: error.config.headers.Authorization ? '[REDACTED]' : undefined,
      } : undefined,
      timestamp: new Date().toISOString(),
      context,
    });

    // Check for common authentication issues
    if (error.response?.status === 401) {
      console.error('[Karrio API] Authentication Error Details:', {
        message: 'The API key may be invalid or expired',
        apiKeyConfigured: API_KEY_EXISTS,
        apiKeyPrefix: API_KEY_PREFIX,
        apiUrl: API_URL,
        responseData: error.response?.data,
      });
    }

    // Check for network/connection issues
    if (error.code === 'ECONNREFUSED' || error.code === 'ENOTFOUND') {
      console.error('[Karrio API] Network Error Details:', {
        message: 'Cannot connect to Karrio platform API',
        errorCode: error.code,
        apiUrl: API_URL,
        suggestion: 'Check if KARRIO_PLATFORM_API_URL is correct and the service is running',
      });
    }

    throw new TRPCError({
      code: error.response?.status === 401 ? "UNAUTHORIZED" : "INTERNAL_SERVER_ERROR",
      message: error.data?.errors?.[0]?.message || error.response?.data?.message || error.message || errorMessage,
      cause: {
        originalError: error.message,
        statusCode: error.response?.status,
        apiResponse: error.response?.data,
        apiUrl: API_URL,
        timestamp: new Date().toISOString(),
      },
    });
  }
}
