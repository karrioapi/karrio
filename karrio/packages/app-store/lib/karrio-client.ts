import { KarrioClient as BaseKarrioClient } from '@karrio/types';

export interface KarrioClientConfig {
  apiKey: string;
  baseURL?: string;
}

/**
 * Factory function to create a Karrio client instance
 */
export function createKarrioClient(apiKey: string, baseURL?: string): BaseKarrioClient {
  return new BaseKarrioClient({
    apiKey,
    basePath: baseURL || process.env.KARRIO_API_URL || 'http://localhost:8000',
  });
}

/**
 * Hook for React components to use Karrio client (if using React)
 */
export function useKarrioClient(apiKey: string, baseURL?: string): BaseKarrioClient {
  // In a real React app, you might want to memoize this
  return createKarrioClient(apiKey, baseURL);
}

// Re-export the main KarrioClient for convenience
export { KarrioClient } from '@karrio/types';
