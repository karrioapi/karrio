import { AddressesApi } from './generated/apis/AddressesApi';
import { APIApi } from './generated/apis/APIApi';
import { CarriersApi } from './generated/apis/CarriersApi';
import { CustomsApi } from './generated/apis/CustomsApi';
import { ParcelsApi } from './generated/apis/ParcelsApi';
import { PickupsApi } from './generated/apis/PickupsApi';
import { ProxyApi } from './generated/apis/ProxyApi';
import { ShipmentsApi } from './generated/apis/ShipmentsApi';
import { TrackersApi } from './generated/apis/TrackersApi';
import { WebhooksApi } from './generated/apis/WebhooksApi';
import { OrdersApi } from './generated/apis/OrdersApi';
import { BatchesApi } from './generated/apis/BatchesApi';
import { DocumentsApi } from './generated/apis/DocumentsApi';
import { ConfigurationParameters } from './generated/runtime';
export * from './generated/runtime';
export * from './generated/models';
export interface KarrioClientInterface {
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
    orders: OrdersApi;
    batches: BatchesApi;
    documents: DocumentsApi;
    config: ConfigurationParameters;
}
export declare class KarrioClient implements KarrioClientInterface {
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
    orders: OrdersApi;
    batches: BatchesApi;
    documents: DocumentsApi;
    config: ConfigurationParameters;
    constructor(clientConfig: ConfigurationParameters);
}
