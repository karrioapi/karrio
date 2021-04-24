import { Address, Customs, Message, Parcel, ParcelDimensionUnitEnum, ParcelWeightUnitEnum, PaymentCurrencyEnum, PaymentPaidByEnum, Shipment } from '@/api';
import { get_address_templates_address_templates_edges_node, get_address_templates_address_templates_edges_node_address, get_customs_info_templates_customs_templates_edges_node, get_customs_info_templates_customs_templates_edges_node_customs, get_logs_logs_edges_node, get_parcel_templates_parcel_templates_edges_node, get_parcel_templates_parcel_templates_edges_node_parcel } from '@/graphql';



export type LogType = get_logs_logs_edges_node;
export type AddressType = Address | get_address_templates_address_templates_edges_node_address
export type ParcelType = Parcel | get_parcel_templates_parcel_templates_edges_node_parcel;
export type CustomsType = Customs | get_customs_info_templates_customs_templates_edges_node_customs;

export type AddressTemplate = get_address_templates_address_templates_edges_node;
export type CustomsTemplateType = get_customs_info_templates_customs_templates_edges_node;
export type ParcelTemplateType = get_parcel_templates_parcel_templates_edges_node;
export type TemplateType = AddressTemplate & ParcelTemplateType & CustomsTemplateType;

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
        .values(PaymentPaidByEnum)
        .filter(key => key.toLowerCase() === key)
));

export const CURRENCY_OPTIONS = Array.from(new Set(
    Object
        .values(PaymentCurrencyEnum)
));

export const DIMENSION_UNITS = Array.from(new Set(
    Object
        .values(ParcelDimensionUnitEnum)
));

export const WEIGHT_UNITS = Array.from(new Set(
    Object
        .values(ParcelWeightUnitEnum)
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
