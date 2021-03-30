import { AddressesApi } from './apis/AddressesApi';
import { APIApi } from './apis/APIApi';
import { CarriersApi } from './apis/CarriersApi';
import { CustomsApi } from './apis/CustomsApi';
import { ParcelsApi } from './apis/ParcelsApi';
import { PickupsApi } from './apis/PickupsApi';
import { ProxyApi } from './apis/ProxyApi';
import { ShipmentsApi } from './apis/ShipmentsApi';
import { TrackersApi } from './apis/TrackersApi';
import { WebhooksApi } from './apis/WebhooksApi';
import { Configuration } from './runtime';

export * from './runtime';
export * from './models';

export interface PurplshipAPI {
    API: APIApi;
    addresses: AddressesApi;
    carriers: CarriersApi;
    customs: CustomsApi;
    parcels: ParcelsApi;
    pickups: PickupsApi;
    proxy: ProxyApi;
    shipments: ShipmentsApi;
    trackers: TrackersApi;
    webhooks: WebhooksApi;
}

export class Purplship implements PurplshipAPI {
    API: APIApi;
    addresses: AddressesApi;
    carriers: CarriersApi;
    customs: CustomsApi;
    parcels: ParcelsApi;
    pickups: PickupsApi;
    proxy: ProxyApi;
    shipments: ShipmentsApi;
    trackers: TrackersApi;
    webhooks: WebhooksApi;
    
    constructor(apiKey: string, host: string) {
        const config = new Configuration({
            basePath: host,
            apiKey: apiKey
        });

        this.API = new APIApi(config);
        this.addresses = new AddressesApi(config);
        this.carriers = new CarriersApi(config);
        this.customs = new CustomsApi(config);
        this.parcels = new ParcelsApi(config);
        this.pickups = new PickupsApi(config);
        this.proxy = new ProxyApi(config);
        this.shipments = new ShipmentsApi(config);
        this.trackers = new TrackersApi(config);
        this.webhooks = new WebhooksApi(config);
    }
}
