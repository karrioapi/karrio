import { ConfigurationParameters, KarrioClient } from './index';

export default function Karrio(apiKey: string, host: string = 'https://api.karrio.io', apiKeyPrefix: string = 'Token') {
  const clientConfig: ConfigurationParameters = {
    basePath: host,
    apiKey: `${apiKeyPrefix} ${apiKey}`,
  };

  return new KarrioClient(clientConfig);
}

Karrio.Client = KarrioClient;
