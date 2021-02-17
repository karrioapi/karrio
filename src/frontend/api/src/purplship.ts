import * as API from './api';
import {Configuration} from './configuration';

export interface PurplshipAPI {
    addresses: API.AddressesApi;
    carriers: API.CarriersApi;
    customs: API.CustomsApi;
    parcels: API.ParcelsApi;
    pickups: API.PickupsApi;
    proxy: API.ProxyApi;
    shipments: API.ShipmentsApi;
    trackers: API.TrackersApi;
    utils: API.UtilsApi;
}

export class Purplship implements PurplshipAPI {
    addresses: API.AddressesApi;
    carriers: API.CarriersApi;
    customs: API.CustomsApi;
    parcels: API.ParcelsApi;
    pickups: API.PickupsApi;
    proxy: API.ProxyApi;
    shipments: API.ShipmentsApi;
    trackers: API.TrackersApi;
    utils: API.UtilsApi;
    
    constructor(apiKey: string, host: string) {
        const config = new Configuration();
        config.basePath = host;
        config.apiKey = apiKey;

        this.addresses = new API.AddressesApi(config);
        this.carriers = new API.CarriersApi(config);
        this.customs = new API.CustomsApi(config);
        this.parcels = new API.ParcelsApi(config);
        this.pickups = new API.PickupsApi(config);
        this.proxy = new API.ProxyApi(config);
        this.shipments = new API.ShipmentsApi(config);
        this.trackers = new API.TrackersApi(config);
        this.utils = new API.UtilsApi(config);
    }
}
