import { Address, CarrierSettings, Customs, Message, Parcel, Payment, Shipment } from '@purplship/purplship';

export interface View {
    path: string
}

export interface UserInfo {
    full_name: string | null;
    email: string | null;
    readonly is_staff: boolean;
}

export interface Connection extends Omit<CarrierSettings, 'id' | 'carrier_name'> {
    id: string | null | undefined;
    carrier_name: CarrierSettings.CarrierNameEnum | 'none';
    [property: string]: any;
}

export interface ConnectionData {
    carrier_name: CarrierSettings.CarrierNameEnum;
    carrier_config: Partial<Connection>;
}

export interface Log {
    id: string;
    requested_at: string;
    response_ms: string;
    path: string;
    view: string;
    view_method: string;
    remote_addr: string;
    host: string;
    method: string;
    query_params: string;
    data: string;
    response: string;
    status_code: string;
}

export interface Template {
    id?: string;
    label?: string;
    is_default?: boolean;
    address?: Address;
    customs?: Customs;
    parcel?: Parcel;
}

export interface PaginatedContent<T> {
    count: Number;
    url?: string | null;
    next?: string | null;
    previous?: string | null;
    results: T[];
    fetched?: boolean;
}

export interface PaginatedLogs extends PaginatedContent<Log> { }
export interface PaginatedShipments extends PaginatedContent<Shipment> { }
export interface PaginatedTemplates extends PaginatedContent<Template> { }
export interface PaginatedConnections extends PaginatedContent<Connection> { }


export enum NotificationType {
    error = "is-danger",
    warning = "is-warning",
    info = "is-info",
    success = "is-success"
}

export interface Notification {
    type: NotificationType;
    message: string | Error | RequestError;
}

export interface LabelData {
    shipment: Shipment;
}

export type Collection<T = string> = {
    [code: string]: T;
};

export type PresetCollection = {
    [carrier_name: string]: {
        [code: string]: Partial<Parcel>
    }
};

export const PAYOR_OPTIONS = Array.from(new Set(
    Object
        .keys(Payment.PaidByEnum)
        .filter(key => key.toLowerCase() === key)
));

export const CURRENCY_OPTIONS = Array.from(new Set(
    Object
        .keys(Payment.CurrencyEnum)
));

export const DIMENSION_UNITS = Array.from(new Set(
    Object
        .keys(Parcel.DimensionUnitEnum)
));

export const WEIGHT_UNITS = Array.from(new Set(
    Object
        .keys(Parcel.WeightUnitEnum)
));

export type ErrorMessage = Message & {
    carrier_id?: string;
    carrier_name?: string;
};

export type FieldError = {
    [key: string]: { code: string; message: string; };
};

export interface APIError {
    error: {
        code: string;
        message?: string;
        details: { messages?: ErrorMessage[]; } & FieldError;
    };
}

export class RequestError extends Error {
    constructor(public data: APIError, ...params: any[]) {
        super(...params);
        if (Error.captureStackTrace) {
            Error.captureStackTrace(this, RequestError)
        }
    }
}

export class DefaultTemplates {
    constructor(private templates: Template[]) { }

    get customs(): Customs | undefined {
        const template = this.templates.find(
            template => template.customs !== undefined && template.customs !== null
        );
        return (template || {}).customs
    }

    get address(): Address | undefined {
        const template = this.templates.find(
            template => template.address !== undefined && template.address !== null
        );
        return (template || {}).address
    }

    get parcel(): Parcel | undefined {
        const template = this.templates.find(
            template => template.parcel !== undefined && template.parcel !== null
        );
        return (template || {}).parcel
    }
}
