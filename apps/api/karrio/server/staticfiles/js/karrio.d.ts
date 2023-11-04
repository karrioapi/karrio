import { KarrioClient } from './index';
declare function Karrio(apiKey: string, host?: string, apiKeyPrefix?: string): KarrioClient;
declare namespace Karrio {
    var Client: typeof KarrioClient;
}
export default Karrio;
