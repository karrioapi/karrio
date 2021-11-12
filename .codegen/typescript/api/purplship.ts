import { ConfigurationParameters, PurplshipClient } from './index';

export default function Purplship(apiKey: string, host: string = 'https://cloud.purplship.com', apiKeyPrefix: string = 'Token') {
  const clientConfig: ConfigurationParameters = {
    basePath: host,
    apiKey: `${apiKeyPrefix} ${apiKey}`,
  };

  return new PurplshipClient(clientConfig);
}

Purplship.Client = PurplshipClient;
