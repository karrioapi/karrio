import { KarrioClient } from '@karrio/types';

export default function Karrio(apiKey: string, host: string = 'https://api.karrio.io', apiKeyPrefix: string = 'Token') {
  const clientConfig = {
    credentials: "include",
    basePath: host,
    apiKey: `${apiKeyPrefix} ${apiKey}`,
    headers: {
      "Accept": "application/json",
      "Content-Type": "application/json",
    },
  };

  return new KarrioClient(clientConfig);
}

Karrio.Client = KarrioClient;
