import * as API from './api';
export interface PurplshipAPI {
    addresses: API.AddressesApi;
    carriers: API.CarriersApi;
    customs: API.CustomsApi;
    parcels: API.ParcelsApi;
    pickups: API.PickupsApi;
    rates: API.RatesApi;
    shipments: API.ShipmentsApi;
    shipping: API.ShippingApi;
    tracking: API.TrackingApi;
    utils: API.UtilsApi;
}
export declare class Purplship implements PurplshipAPI {
    addresses: API.AddressesApi;
    carriers: API.CarriersApi;
    customs: API.CustomsApi;
    parcels: API.ParcelsApi;
    pickups: API.PickupsApi;
    rates: API.RatesApi;
    shipments: API.ShipmentsApi;
    shipping: API.ShippingApi;
    tracking: API.TrackingApi;
    utils: API.UtilsApi;
    constructor(apiKey: string, host: string);
}
