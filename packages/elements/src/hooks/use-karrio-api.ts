import { useKarrio } from '../provider/karrio-provider';
import { useEffect, useState } from 'react';
import axios from 'axios';

interface GraphQLRequest {
  query: string;
  variables?: Record<string, any>;
}

interface KarrioAPI {
  graphql: (request: GraphQLRequest) => Promise<any>;
  baseUrl: string;
}

/**
 * Hook to access the Karrio API with authentication
 * Provides methods for making GraphQL requests to the Karrio API
 */
export function useKarrioAPI(): KarrioAPI {
  const { isAuthenticated, accessToken, sessionData } = useKarrio();
  const [baseUrl, setBaseUrl] = useState<string>('');

  useEffect(() => {
    // Get the API URL from environment variables
    const apiUrl = process.env.NEXT_PUBLIC_KARRIO_API_URL || 'https://api.karrio.io';
    setBaseUrl(apiUrl);
  }, []);

  /**
   * Make a GraphQL request to the Karrio API using axios
   */
  const graphql = async (request: GraphQLRequest) => {
    if (!baseUrl) {
      throw new Error('API URL not configured');
    }

    // If not authenticated or session is not available, throw an error
    if (!isAuthenticated || !accessToken) {
      console.error('Authentication required, authenticated:', isAuthenticated);
      throw new Error('Authentication required');
    }

    // Get optional data from session
    const testMode = sessionData?.testMode;
    const orgId = sessionData?.orgId;

    // Debugging session data
    console.log('useKarrioAPI session info:', {
      isAuthenticated,
      testMode,
      orgId,
      accessTokenPresent: !!accessToken,
      sessionDataKeys: sessionData ? Object.keys(sessionData) : []
    });

    const headers = {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${accessToken}`,
      ...(orgId ? { 'x-org-id': orgId } : {}),
      ...(testMode ? { 'x-test-mode': 'true' } : {}),
    };

    console.log('Request headers:', headers);

    try {
      const response = await axios({
        method: 'POST',
        url: `${baseUrl}/graphql/`,
        headers,
        data: {
          query: request.query,
          variables: request.variables || {},
        }
      });

      return response.data;
    } catch (error) {
      if (axios.isAxiosError(error)) {
        console.error('GraphQL request failed:', error.response?.data || error.message);
        throw new Error(`GraphQL request failed: ${error.response?.data || error.message}`);
      }
      console.error('Unknown error in GraphQL request:', error);
      throw error;
    }
  };

  return {
    graphql,
    baseUrl,
  };
}
