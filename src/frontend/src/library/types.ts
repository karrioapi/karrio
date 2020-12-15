import { Message, Parcel, Payment } from "@purplship/purplship";

export interface View {
    path: string
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
