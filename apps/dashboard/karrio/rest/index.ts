export * from './generated/api';
import axios, { AxiosInstance, AxiosRequestHeaders } from 'axios';
import { Configuration, ConfigurationParameters } from './generated/configuration';
import {
  AddressesApi,
  APIApi,
  CarriersApi,
  CustomsApi,
  ParcelsApi,
  PickupsApi,
  ProxyApi,
  ShipmentsApi,
  TrackersApi,
  OrdersApi,
  WebhooksApi,
  BatchesApi,
  DocumentsApi,
} from './generated/api';


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
  orders: OrdersApi;
  webhooks: WebhooksApi;
  batches: BatchesApi;
  documents: DocumentsApi;
  config: ConfigurationParameters;
}

export class KarrioClient implements KarrioClientInterface {
  API: APIApi;
  addresses: AddressesApi;
  carriers: CarriersApi;
  customs: CustomsApi;
  parcels: ParcelsApi;
  pickups: PickupsApi;
  proxy: ProxyApi;
  shipments: ShipmentsApi;
  trackers: TrackersApi;
  orders: OrdersApi;
  webhooks: WebhooksApi;
  documents: DocumentsApi;
  batches: BatchesApi;
  config: ConfigurationParameters;
  axios: AxiosInstance;

  constructor({ headers, ...clientConfig }: ConfigurationParameters & { headers?: AxiosRequestHeaders }) {
    const config = new Configuration(clientConfig);
    const axiosInstance = axios.create({ baseURL: config.basePath, headers });

    this.axios = axiosInstance;
    this.config = clientConfig;
    this.API = new APIApi(config, config.basePath, axiosInstance);
    this.addresses = new AddressesApi(config, config.basePath, axiosInstance);
    this.carriers = new CarriersApi(config, config.basePath, axiosInstance);
    this.customs = new CustomsApi(config, config.basePath, axiosInstance);
    this.parcels = new ParcelsApi(config, config.basePath, axiosInstance);
    this.pickups = new PickupsApi(config, config.basePath, axiosInstance);
    this.proxy = new ProxyApi(config, config.basePath, axiosInstance);
    this.shipments = new ShipmentsApi(config, config.basePath, axiosInstance);
    this.trackers = new TrackersApi(config, config.basePath, axiosInstance);
    this.orders = new OrdersApi(config, config.basePath, axiosInstance);
    this.webhooks = new WebhooksApi(config, config.basePath, axiosInstance);
    this.documents = new DocumentsApi(config, config.basePath, axiosInstance);
    this.batches = new BatchesApi(config, config.basePath, axiosInstance);
  }
}
