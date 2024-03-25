import * as api from './rest/api';
import * as graph from './graphql/index';
import * as ee from './graphql/ee/index';

export {
    CarrierSettingsCarrierNameEnum,
    CustomsIncotermEnum,
    WebhookEnabledEventsEnum,
    OrderStatusEnum,
} from './rest/api';

export type MessageType = graph.get_tracker_tracker_messages;
export type LogType = graph.get_logs_logs_edges_node;
export type EventType = graph.get_events_events_edges_node;
export type AddressType = graph.get_shipment_shipment_shipper;
export type CommodityType = (
    graph.get_order_order_line_items |
    graph.get_shipment_shipment_customs_commodities |
    graph.get_shipment_shipment_parcels_items
) & {
    unfulfilled_quantity?: number | null;
};
export type DutyType = graph.get_shipment_shipment_customs_duty;
export type CustomsType = graph.get_shipment_shipment_customs & {
    commodities: CommodityType[];
    duty?: DutyType;
    duty_billing_address?: AddressType | null;
    id?: string;
};
export type ParcelType = graph.get_shipment_shipment_parcels & {
    items: CommodityType[];
};
export type ManifestType = graph.GetManifests_manifests_edges_node;
export type TrackingEventType = graph.get_tracker_tracker_events;
export type TrackerType = graph.get_tracker_tracker & {
    events: TrackingEventType[];
    messages?: MessageType[];
};
export type ChargeType = graph.get_shipment_shipment_selected_rate_extra_charges;
export type RateType = graph.get_shipment_shipment_rates;
export type PaymentType = graph.get_shipment_shipment_payment;
export type ShipmentType = graph.get_shipment_shipment & {
    parcels: ParcelType[];
    shipper: AddressType;
    recipient: AddressType;
    billing_address?: AddressType | null;
    customs?: CustomsType | null;
    rates?: RateType[];
    messages?: MessageType[];
    selected_rate?: RateType;
    payment?: PaymentType;
};
export interface OrderType extends graph.get_order_order {
    line_items: graph.get_order_order_line_items[];
    shipments: ShipmentType[];
}

export type AddressTemplateType = graph.get_address_templates_address_templates_edges_node & {
    address: AddressType;
};
export type CustomsTemplateType = graph.get_customs_info_templates_customs_templates_edges_node & {
    customs: CustomsType;
};
export type ParcelTemplateType = graph.get_parcel_templates_parcel_templates_edges_node & {
    parcel: ParcelType;
};
export type TemplateType = AddressTemplateType & ParcelTemplateType & CustomsTemplateType;

export type ServiceLevelType = graph.CreateServiceLevelInput & graph.UpdateServiceLevelInput;

export type LabelTemplateType = graph.get_user_connections_user_connections_GenericSettingsType_label_template;

export type DocumentTemplateType = graph.get_document_template_document_template;

export interface WebhookType extends graph.get_webhooks_webhooks_edges_node { }

export type TenantType = {
    schema_name: string;
    api_domains: string[];
}

export interface View {
    path: string
}

export enum NotificationType {
    error = "is-danger",
    warning = "is-warning",
    info = "is-info",
    success = "is-success"
}

export interface Notification {
    type?: NotificationType;
    message: string | Error | RequestError | MessageType[] | ErrorType[];
}

export interface LabelData {
    shipment: ShipmentType;
}

export type Collection<T = string> = {
    [code: string]: T;
};

export type PresetCollection = {
    [carrier_name: string]: {
        [code: string]: Partial<ParcelType>
    }
};

export const PAYOR_OPTIONS = Array.from(new Set(
    Object
        .values(graph.PaidByEnum)
        .filter(key => (key as string).toLowerCase() === key)
));

export const CURRENCY_OPTIONS = Array.from(new Set(
    Object
        .values(graph.CurrencyCodeEnum)
));

export const COUNTRY_OPTIONS = Array.from(new Set(
    Object
        .values(graph.CountryCodeEnum)
));

export const DIMENSION_UNITS = Array.from(new Set(
    Object
        .values(graph.DimensionUnitEnum)
));

export const WEIGHT_UNITS = Array.from(new Set(
    Object
        .values(graph.WeightUnitEnum)
));

export const EVENT_TYPES: string[] = Array.from(new Set(
    Object
        .values(api.WebhookEnabledEventsEnum)
));

export const SHIPMENT_STATUSES: string[] = Array.from(new Set(
    Object
        .values(graph.ShipmentStatusEnum)
));

export const ORDER_STATUSES: string[] = Array.from(new Set(
    Object
        .values(graph.OrderStatus)
));

export const TRACKER_STATUSES: string[] = Array.from(new Set(
    Object
        .values(graph.TrackerStatusEnum)
));

export const CARRIER_NAMES: string[] = Array.from(new Set(
    Object
        .values(api.CarrierSettingsCarrierNameEnum)
));

export const INCOTERMS: string[] = Array.from(new Set(
    Object
        .values(api.CustomsIncotermEnum)
));

export const CUSTOMS_CONTENT_TYPES: string[] = Array.from(new Set(
    Object
        .values(graph.CustomsContentTypeEnum)
));

export const DOCUMENT_RELATED_OBJECTS: string[] = Array.from(new Set(
    Object
        .values(graph.TemplateRelatedObject)
));

export const LABEL_TYPES: string[] = Array.from(new Set(
    Object
        .values(graph.LabelTypeEnum)
));

export type requestArgs = {
    variables?: Record<string, any>;
    data?: Record<string, any>;
    operationName?: string;
    url?: string;
} & Record<string, any>;

export type ErrorMessage = MessageType & {
    carrier_id?: string;
    carrier_name?: string;
};

export type FieldError = {
    [key: string]: { code: string; message: string | string[]; };
};

export interface APIError {
    errors?: {
        code: string;
        message?: string;
        details: { messages?: ErrorMessage[]; } & FieldError;
    }[],
    messages?: {
        code: string;
        message?: string;
        carrier_id?: string;
        carrier_name?: string;
        details: { messages?: ErrorMessage[]; } & FieldError;
    }[],
}

export class RequestError extends Error {
    constructor(public data: APIError, ...params: any[]) {
        super(...params);
        if (Error.captureStackTrace) {
            Error.captureStackTrace(this, RequestError)
        }
    }
}

export class ErrorType {
    constructor(
        public field: string,
        public messages: string[]
    ) { }
}

export const HTTP_STATUS_CODES = [
    200,
    201,
    204,
    207,
    400,
    401,
    403,
    404,
    409,
    500,
];

export const HTTP_METHODS = [
    "GET",
    "POST",
    "PATCH",
    "DELETE",
];

export enum NoneEnum { none = "none" };

export type dataT<T> = { data?: T };
export type AccountContextDataType = {
    data: {
        user: graph.GetUser_user,
        workspace_config: graph.GetWorkspaceConfig_workspace_config,
    }
};
export type OrgContextDataType = {
    data: {
        organizations?: ee.get_organizations_organizations[]
    }
};

export type SubscriptionType = {
    status: string;
    is_owner: boolean;
    period_end: string;
    subscription_type: string;
};

export type PortalSessionType = {
    url: string;
}

export type UserType = graph.GetUser_user;

export interface Metadata {
    HOST: string;
    ADMIN: string;
    OPENAPI: string;
    GRAPHQL: string;
    VERSION: string;
    APP_NAME: string;

    AUDIT_LOGGING: boolean;
    ALLOW_SIGNUP: boolean;
    ALLOW_ADMIN_APPROVED_SIGNUP: boolean;
    ALLOW_MULTI_ACCOUNT: boolean;
    ADMIN_DASHBOARD: boolean;
    ORDERS_MANAGEMENT: boolean;
    APPS_MANAGEMENT: boolean;
    DOCUMENTS_MANAGEMENT: boolean;
    DATA_IMPORT_EXPORT: boolean;
    CUSTOM_CARRIER_DEFINITION: boolean;
    MULTI_ORGANIZATIONS: boolean;
    PERSIST_SDK_TRACING: boolean;
    ORG_LEVEL_BILLING: boolean;
    TENANT_LEVEL_BILLING: boolean;
    WORKFLOW_MANAGEMENT: boolean;
};

export interface References {
    HOST: string;
    ADMIN: string;
    OPENAPI: string;
    GRAPHQL: string;
    VERSION: string;
    APP_NAME: string;
    APP_WEBSITE: string;

    AUDIT_LOGGING: boolean;
    ALLOW_SIGNUP: boolean;
    ALLOW_ADMIN_APPROVED_SIGNUP: boolean;
    ALLOW_MULTI_ACCOUNT: boolean;
    ADMIN_DASHBOARD: boolean;
    ORDERS_MANAGEMENT: boolean;
    APPS_MANAGEMENT: boolean;
    DOCUMENTS_MANAGEMENT: boolean;
    DATA_IMPORT_EXPORT: boolean;
    CUSTOM_CARRIER_DEFINITION: boolean;
    MULTI_ORGANIZATIONS: boolean;
    PERSIST_SDK_TRACING: boolean;
    ORG_LEVEL_BILLING: boolean;
    TENANT_LEVEL_BILLING: boolean;
    WORKFLOW_MANAGEMENT: boolean;

    ADDRESS_AUTO_COMPLETE: Collection;
    countries: Collection;
    currencies: Collection;
    carriers: Collection;
    custom_carriers: Collection;
    states: Collection<Collection>;
    options: Collection<Collection<{ code: string, type: string }>>;
    services: Collection<Collection>;
    option_names: Collection<Collection>;
    service_names: Collection<Collection>;
    package_presets: Collection<Collection>;
    packaging_types: Collection<Collection>;
    carrier_capabilities: Collection<string[]>;
    service_levels: Collection<ServiceLevelType[]>;
    connection_configs: Collection<Collection<Collection>>;
}

export type SessionType<T = {}> = T & {
    accessToken: string,
    testMode?: boolean,
    orgId?: string,
    error?: string,
};

export const CARRIER_THEMES: Collection = {
    'aramex': 'is-aramex',
    'australiapost': 'is-australiapost',
    'boxknight': 'is-boxknight',
    'canadapost': 'is-canadapost',
    'canpar': 'is-canpar',
    'dicom': 'is-dicom',
    'dhl_express': 'is-dhl',
    'dhl_poland': 'is-dhl',
    'dhl_universal': 'is-dhl',
    'dpd': 'is-dpd',
    'dpdhl': 'is-dhl',
    'dhl_parcel_de': 'is-dhl',
    'eshipper': 'is-eshipper',
    'easypost': 'is-easypost',
    'geodis': 'is-geodis',
    'laposte': 'is-laposte',
    'nationex': 'is-nationex',
    'fedex': 'is-fedex',
    'fedex_ws': 'is-fedex',
    'freightcom': 'is-freightcom',
    'generic': 'is-generic',
    'purolator': 'is-purolator',
    'roadie': 'is-roadie',
    'royalmail': 'is-royalmail',
    'sendle': 'is-sendle',
    'sf_express': 'is-sf_express',
    'tnt': 'is-tnt',
    'ups': 'is-ups',
    'usps': 'is-usps',
    'usps_international': 'is-usps',
    'yanwen': 'is-yanwen',
    'yunexpress': 'is-yunexpress',
};

export const CARRIER_IMAGES: Collection = {
    'amazon_mws': 'amazon_mws',
    'apc': 'generic',
    'asendia': 'generic',
    'asendia_us': 'generic',
    'aramex': 'aramex',
    'australiapost': 'australiapost',
    'axlehire': 'generic',
    'better_trucks': 'generic',
    'bond': 'generic',
    'canadapost': 'canadapost',
    'canpar': 'canpar',
    'cdl': 'generic',
    'chronopost': 'generic',
    'cloudsort': 'generic',
    'courier_express': 'generic',
    'courierplease': 'generic',
    'daipost': 'generic',
    'deutschepost': 'generic',
    'deutschepost_uk': 'generic',
    'dicom': 'dicom',
    'dhl_ecom_asia': 'dhl_express',
    'dhl_ecom': 'dhl_express',
    'dhl_express': 'dhl_express',
    'dhl_poland': 'dhl_express',
    'dpdhl': 'dhl_express',
    'dhl_parcel_de': 'dhl_express',
    'dhl_universal': 'dhl_universal',
    'dpd': 'dpd',
    'dpd_uk': 'dpd',
    'epost': 'generic',
    'estafeta': 'generic',
    'fastway': 'generic',
    'fedex': 'fedex',
    'fedex_ws': 'fedex',
    'fedex_mail': 'fedex',
    'fedex_sameday_city': 'fedex',
    'fedex_smartpost': 'fedex',
    'firstmile': 'generic',
    'globegistics': 'generic',
    'gso': 'generic',
    'hermes': 'generic',
    'interlink': 'generic',
    'jppost': 'generic',
    'kuroneko_yamato': 'generic',
    'lasership': 'generic',
    'loomis': 'generic',
    'lso': 'generic',
    'newgistics': 'generic',
    'ontrac': 'generic',
    'osm': 'generic',
    'parcelforce': 'generic',
    'parcll': 'generic',
    'passport': 'generic',
    'postnl': 'generic',
    'purolator': 'purolator',
    'royalmail': 'royalmail',
    'seko': 'generic',
    'sendle': 'sendle',
    'sfexpress': 'sfexpress',
    'speedee': 'generic',
    'startrack': 'generic',
    'tforce': 'generic',
    'uds': 'generic',
    'ups': 'ups',
    'ups_iparcel': 'ups',
    'ups_mail_innovations': 'ups',
    'usps': 'usps',
    'veho': 'generic',
    'yanwen': 'yanwen',
    'eshipper': 'generic',
    'easypost': 'generic',
    'freightcom': 'generic',
    'generic': 'generic',
    'sf_express': 'sf_express',
    'tnt': 'tnt',
    'usps_international': 'usps',
    'yunexpress': 'yunexpress',
    'boxknight': 'boxknight',
    'geodis': 'geodis',
    'laposte': 'laposte',
    'nationex': 'nationex',
    'roadie': 'roadie',
}

export const IMAGES = (
    Object
        .entries(CARRIER_IMAGES)
        .filter(([_, val]) => val !== 'generic')
        .map(([key, _]) => key)
);

export const DEFAULT_ADDRESS_CONTENT = {
    address_line1: '',
    address_line2: '',
    residential: false
} as Partial<AddressType>;

export const DEFAULT_PARCEL_CONTENT: Partial<ParcelType> = {
    weight: 1.0,
    width: 33.7,
    height: 18.2,
    length: 10.0,
    is_document: false,
    packaging_type: "your_packaging",
    weight_unit: graph.WeightUnitEnum.KG,
    dimension_unit: graph.DimensionUnitEnum.CM,
    items: [],
};

export const DEFAULT_COMMODITY_CONTENT: Partial<CommodityType> = {
    weight: 1,
    quantity: 1,
    weight_unit: graph.WeightUnitEnum.KG,
};

export const DEFAULT_CUSTOMS_CONTENT: Partial<CustomsType> = {
    duty: { paid_by: graph.PaidByEnum.recipient } as any,
    certify: true,
    commodities: [DEFAULT_COMMODITY_CONTENT as CommodityType],
    incoterm: graph.IncotermCodeEnum.DDU,
    content_type: graph.CustomsContentTypeEnum.merchandise,
    options: {}
};
