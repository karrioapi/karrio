import { AddressesApi } from './generated/apis/AddressesApi';
import { APIApi } from './generated/apis/APIApi';
import { CarriersApi } from './generated/apis/CarriersApi';
import { ParcelsApi } from './generated/apis/ParcelsApi';
import { PickupsApi } from './generated/apis/PickupsApi';
import { ProxyApi } from './generated/apis/ProxyApi';
import { ShipmentsApi } from './generated/apis/ShipmentsApi';
import { TrackersApi } from './generated/apis/TrackersApi';
import { WebhooksApi } from './generated/apis/WebhooksApi';
import { OrdersApi } from './generated/apis/OrdersApi';
import { BatchesApi } from './generated/apis/BatchesApi';
import { DocumentsApi } from './generated/apis/DocumentsApi';
import { ManifestsApi } from './generated/apis/ManifestsApi';
import { Configuration, ConfigurationParameters } from './generated/runtime';

export * from './generated/runtime';
export * from './generated/models';

export interface KarrioClientInterface {
  API: APIApi;
  addresses: AddressesApi;
  carriers: CarriersApi;
  parcels: ParcelsApi;
  pickups: PickupsApi;
  proxy: ProxyApi;
  shipments: ShipmentsApi;
  trackers: TrackersApi;
  webhooks: WebhooksApi;
  orders: OrdersApi;
  batches: BatchesApi;
  documents: DocumentsApi;
  manifest: ManifestsApi;
  config: ConfigurationParameters;
}

export class KarrioClient implements KarrioClientInterface {
  API: APIApi;
  addresses: AddressesApi;
  carriers: CarriersApi;
  parcels: ParcelsApi;
  pickups: PickupsApi;
  proxy: ProxyApi;
  shipments: ShipmentsApi;
  trackers: TrackersApi;
  webhooks: WebhooksApi;
  orders: OrdersApi;
  batches: BatchesApi;
  documents: DocumentsApi;
  manifest: ManifestsApi;
  config: ConfigurationParameters;

  constructor(clientConfig: ConfigurationParameters) {
    const config = new Configuration({
      credentials: "include",
      headers: {
        "Accept": "application/json",
        "Content-Type": "application/json",
      },
      ...clientConfig
    });

    this.config = clientConfig;
    this.API = new APIApi(config);
    this.addresses = new AddressesApi(config);
    this.carriers = new CarriersApi(config);
    this.parcels = new ParcelsApi(config);
    this.pickups = new PickupsApi(config);
    this.proxy = new ProxyApi(config);
    this.shipments = new ShipmentsApi(config);
    this.trackers = new TrackersApi(config);
    this.webhooks = new WebhooksApi(config);
    this.orders = new OrdersApi(config);
    this.manifest = new ManifestsApi(config);
    this.batches = new BatchesApi(config);
    this.documents = new DocumentsApi(config);
  }
}
