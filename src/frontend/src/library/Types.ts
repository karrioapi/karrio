import { Parcel, Payment } from "@purplship/purplship";

export interface View {
    path: string
}

export type Collection = {
    [code: string]: string;
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
